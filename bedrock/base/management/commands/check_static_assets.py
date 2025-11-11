# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Management command to verify that collected static assets are available on a deployed site"""

from __future__ import annotations

import concurrent.futures
import json
import posixpath
import time
from collections.abc import Iterable
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from urllib.parse import urljoin, urlparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import requests

DEFAULT_TIMEOUT = 10
# Default concurrency keeps load manageable when probing cold CDN caches or direct origin checks
DEFAULT_MAX_WORKERS = 8
DEFAULT_RETRY_COUNT = 2
DEFAULT_RETRY_BACKOFF = 1.0
PROGRESS_STEP = 50
USER_AGENT = "bedrock-asset-check/1.0"


@dataclass
class CheckResult:
    asset_path: str
    url: str
    status: int | None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.status is not None and 200 <= self.status < 300


class Command(BaseCommand):
    help = "Fetch each asset listed in the staticfiles manifest from the origin and CDN hosts, reporting any missing files."

    def add_arguments(self, parser):
        parser.add_argument(
            "--origin-host",
            required=True,
            help="Base URL (including scheme) of the origin server, e.g. https://origin.example.com",
        )
        parser.add_argument(
            "--cdn-host",
            required=True,
            help="Base URL (including scheme) of the CDN, e.g. https://www.example.com",
        )
        parser.add_argument(
            "--manifest-path",
            required=True,
            help="Path to the staticfiles manifest generated for the deployed release.",
        )
        parser.add_argument(
            "--timeout",
            type=float,
            default=DEFAULT_TIMEOUT,
            help="Per-request timeout in seconds (default: %(default)s)",
        )
        parser.add_argument(
            "--max-workers",
            type=int,
            default=DEFAULT_MAX_WORKERS,
            help="Number of concurrent HTTP requests per host (default: %(default)s)",
        )
        parser.add_argument(
            "--method",
            choices=("head", "get"),
            default="head",
            help="HTTP method to attempt first. HEAD falls back to GET on 405 responses.",
        )
        parser.add_argument(
            "--skip-pattern",
            action="append",
            default=[],
            help="Glob pattern(s) of asset paths to skip (match against hashed paths in the manifest).",
        )
        parser.add_argument(
            "--retry-count",
            type=int,
            default=DEFAULT_RETRY_COUNT,
            help="Number of retries for transient network errors per asset request (default: %(default)s)",
        )
        parser.add_argument(
            "--retry-backoff",
            type=float,
            default=DEFAULT_RETRY_BACKOFF,
            help="Initial backoff delay in seconds between retries; doubles after each attempt (default: %(default)s)",
        )

    def handle(self, *args, **options):
        origin_host = self._normalize_host(options["origin_host"], "origin-host")
        cdn_host = self._normalize_host(options["cdn_host"], "cdn-host")

        manifest_path = self._resolve_manifest_path(options.get("manifest_path"))
        asset_paths = self._load_manifest_asset_paths(manifest_path)
        skip_patterns = options.get("skip_pattern") or []
        asset_paths, skipped = self._apply_skip_patterns(asset_paths, skip_patterns)
        static_prefix = self._static_prefix(settings.STATIC_URL)

        if skipped:
            self.stdout.write("Skipping {} asset(s) due to skip-patterns: {}".format(len(skipped), ", ".join(sorted(skip_patterns))))

        self.stdout.write(f"Checking {len(asset_paths)} assets found in {manifest_path} (static prefix '{static_prefix or '<root>'}').")

        method = (options.get("method") or "head").lower()
        timeout = options.get("timeout", DEFAULT_TIMEOUT)
        max_workers = options.get("max_workers", DEFAULT_MAX_WORKERS)
        if max_workers < 1:
            raise CommandError("--max-workers must be >= 1")

        retry_count = options.get("retry_count")
        if retry_count is None:
            retry_count = DEFAULT_RETRY_COUNT
        if retry_count < 0:
            raise CommandError("--retry-count must be >= 0")

        retry_backoff = options.get("retry_backoff")
        if retry_backoff is None:
            retry_backoff = DEFAULT_RETRY_BACKOFF
        if retry_backoff <= 0:
            raise CommandError("--retry-backoff must be > 0")

        failures: list[tuple[str, CheckResult]] = []

        for label, host in (("origin", origin_host), ("cdn", cdn_host)):
            asset_total = len(asset_paths)
            progress_step = max(1, min(PROGRESS_STEP, asset_total)) if asset_total else 0

            if asset_total:
                self.stdout.write(
                    f"{label.capitalize()} host {host}: checking {asset_total} assets",
                    ending="",
                )

            start_time = time.perf_counter()

            results = self._check_host(
                base_url=host,
                static_prefix=static_prefix,
                asset_paths=asset_paths,
                method=method,
                timeout=timeout,
                max_workers=max_workers,
                asset_total=asset_total,
                progress_step=progress_step,
                retry_count=retry_count,
                retry_backoff=retry_backoff,
                stdout=self.stdout if asset_total else None,
            )

            elapsed = time.perf_counter() - start_time
            if asset_total:
                self.stdout.write("")  # finish progress line

            host_failures = [result for result in results if not result.ok]
            failures.extend((label, result) for result in host_failures)

            rate = (asset_total / elapsed) if asset_total and elapsed > 0 else 0
            duration = f"{elapsed:.1f}s" if elapsed else "0.0s"
            rate_str = f", ~{rate:.1f} req/s" if rate else ""
            self.stdout.write(
                f"{label.capitalize()} host {host}: {len(results) - len(host_failures)} OK, {len(host_failures)} failed (took {duration}{rate_str})"
            )

            if host_failures:
                self.stderr.write(self.style.ERROR(f"{label.capitalize()} host {host} failures:"))
                for failure in host_failures:
                    message = self._format_failure(failure)
                    self.stderr.write(f" * {message}")

        if failures:
            summary = ", ".join(f"{label}:{failure.asset_path}" for label, failure in failures)
            raise CommandError(f"Asset availability check detected {len(failures)} failures: {summary}")

        self.stdout.write(self.style.SUCCESS("All assets verified successfully."))

    def _resolve_manifest_path(self, manifest_option: str) -> Path:
        manifest_path = Path(manifest_option)
        if not manifest_path.is_file():
            raise CommandError(f"Manifest file not found at {manifest_path}")

        return manifest_path

    def _load_manifest_asset_paths(self, manifest_path: Path) -> list[str]:
        try:
            with manifest_path.open("r", encoding="utf-8") as fp:
                manifest_data = json.load(fp)
        except json.JSONDecodeError as exc:
            raise CommandError(f"Unable to parse manifest: {exc}") from exc

        if isinstance(manifest_data, dict) and "paths" in manifest_data:
            paths = manifest_data["paths"]
        else:
            paths = manifest_data

        if not isinstance(paths, dict):
            raise CommandError("Unexpected manifest structure: expected a mapping of asset paths")

        asset_values = [value for value in paths.values() if isinstance(value, str)]
        if not asset_values:
            raise CommandError("Manifest does not contain any asset entries")

        return sorted(set(asset_values))

    def _apply_skip_patterns(
        self,
        asset_paths: list[str],
        patterns: list[str],
    ) -> tuple[list[str], set[str]]:
        if not patterns:
            return asset_paths, set()

        remaining = []
        skipped = set()
        for asset in asset_paths:
            if any(fnmatch(asset, pattern) for pattern in patterns):
                skipped.add(asset)
                continue
            remaining.append(asset)

        return remaining, skipped

    def _static_prefix(self, static_url: str) -> str:
        parsed = urlparse(static_url)
        if parsed.scheme and parsed.netloc:
            raw_path = parsed.path
        else:
            raw_path = static_url

        raw_path = raw_path.strip()
        if not raw_path:
            return ""

        return raw_path.strip("/")

    def _normalize_host(self, host_value: str, option_name: str) -> str:
        parsed = urlparse(host_value)
        if not parsed.scheme or not parsed.netloc:
            raise CommandError(f"--{option_name} must include a scheme and hostname: '{host_value}'")

        if parsed.username or parsed.password:
            raise CommandError(f"--{option_name} must not include credentials")

        if parsed.query or parsed.params or parsed.fragment:
            raise CommandError(f"--{option_name} must not include query strings or fragments")

        # Disallow nested paths beyond "/" to avoid surprising base URLs.
        cleaned_path = parsed.path.rstrip("/")
        if isinstance(cleaned_path, str) and cleaned_path:
            raise CommandError(f"--{option_name} must not include a path component: '{parsed.path}'")

        normalized = f"{parsed.scheme}://{parsed.netloc}"

        return normalized

    def _check_host(
        self,
        *,
        base_url: str,
        static_prefix: str,
        asset_paths: Iterable[str],
        method: str,
        timeout: float,
        max_workers: int,
        asset_total: int | None = None,
        progress_step: int | None = None,
        retry_count: int = 0,
        retry_backoff: float = 1.0,
        stdout=None,
    ) -> list[CheckResult]:
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
            }
        )

        results: list[CheckResult] = []
        asset_list = list(asset_paths)
        total_items = asset_total if asset_total is not None else len(asset_list)
        step = max(1, progress_step) if progress_step else 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_asset = {
                executor.submit(
                    self._fetch_asset,
                    session,
                    base_url,
                    static_prefix,
                    asset,
                    method,
                    timeout,
                    retry_count,
                    retry_backoff,
                ): asset
                for asset in asset_list
            }

            processed = 0

            for future in concurrent.futures.as_completed(future_to_asset):
                asset = future_to_asset[future]
                try:
                    result = future.result()
                except Exception as exc:  # pragma: no cover - defensive
                    result = CheckResult(
                        asset_path=asset,
                        url=self._build_url(base_url, static_prefix, asset),
                        status=None,
                        error=str(exc),
                    )

                results.append(result)

                if stdout and total_items:
                    processed += 1
                    if processed == total_items or (step and processed % step == 0):
                        stdout.write(".", ending="")

        # Preserve deterministic ordering for ease of reading logs.
        results.sort(key=lambda item: item.asset_path)
        return results

    def _fetch_asset(
        self,
        session: requests.Session,
        base_url: str,
        static_prefix: str,
        asset: str,
        method: str,
        timeout: float,
        retry_count: int,
        retry_backoff: float,
    ) -> CheckResult:
        url = self._build_url(base_url, static_prefix, asset)
        request_method = method.lower()
        retryable_exceptions = (requests.Timeout, requests.ConnectionError)
        delay = retry_backoff
        last_error: str | None = None

        for attempt in range(retry_count + 1):
            try:
                response = session.request(
                    request_method,
                    url,
                    timeout=timeout,
                    allow_redirects=False,
                )

                if request_method == "head" and response.status_code in (301, 302, 303, 307, 308):
                    # If we unexpectedly get a redirect on HEAD, follow up with GET to confirm availability.
                    response = session.get(url, timeout=timeout, allow_redirects=False)

                elif request_method == "head" and not 200 <= response.status_code < 300:
                    # Re-check with GET for CDNs that behave differently for HEAD requests.
                    response = session.get(url, timeout=timeout, allow_redirects=False)

                status = response.status_code
                if 200 <= status < 300:
                    error = None
                elif 300 <= status < 400:
                    location = response.headers.get("Location", "")
                    target = location or "unknown location"
                    error = f"Redirected to {target}"
                else:
                    error = response.reason or f"HTTP {status}"

                return CheckResult(asset_path=asset, url=url, status=status, error=error)

            except requests.RequestException as exc:
                error = str(exc)
                should_retry = attempt < retry_count and isinstance(exc, retryable_exceptions)
                if should_retry:
                    time.sleep(delay)
                    delay *= 2
                    continue

                last_error = error
                break

        return CheckResult(asset_path=asset, url=url, status=None, error=last_error or "Request failed after retries")

    def _build_url(self, base_url: str, static_prefix: str, asset: str) -> str:
        base = base_url.rstrip("/") + "/"
        if static_prefix:
            asset_path = posixpath.join(static_prefix, asset)
        else:
            asset_path = asset

        # urljoin handles redundant slashes cleanly.
        return urljoin(base, asset_path)

    def _format_failure(self, result: CheckResult) -> str:
        if result.status is None:
            reason = result.error or "Unknown error"
        else:
            status_text = f"HTTP {result.status}"
            detail = result.error.strip() if result.error else ""
            reason = f"{status_text}: {detail}".rstrip(": ")

        return f"{result.url} ({result.asset_path}) — {reason}"
