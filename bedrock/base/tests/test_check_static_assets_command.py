# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
from types import MethodType

from django.core.management.base import CommandError

import pytest
import requests

import bedrock.base.management.commands.check_static_assets as asset_command
from bedrock.base.management.commands.check_static_assets import (
    CheckResult,
    Command,
)


def build_command():
    return Command()


def test_static_prefix_handles_various_urls(settings):
    command = build_command()

    assert command._static_prefix("/media/") == "media"
    assert command._static_prefix("media/") == "media"
    assert command._static_prefix("") == ""
    assert command._static_prefix("https://cdn.example.com/assets/") == "assets"


def test_build_url_joins_prefix_and_asset():
    command = build_command()

    assert command._build_url("https://origin.example.com", "media", "css/app.css") == "https://origin.example.com/media/css/app.css"
    assert command._build_url("https://cdn.example.com", "", "img/logo.svg") == "https://cdn.example.com/img/logo.svg"


def test_normalize_host_validates_scheme():
    command = build_command()

    with pytest.raises(CommandError):
        command._normalize_host("example.com", "origin-host")

    assert command._normalize_host("https://example.com/", "origin-host") == "https://example.com"
    with pytest.raises(CommandError):
        command._normalize_host("https://example.com/path/", "cdn-host")
    with pytest.raises(CommandError):
        command._normalize_host("https://example.com?foo=bar", "cdn-host")


def test_load_manifest_asset_paths(tmp_path, settings):
    settings.STATIC_ROOT = tmp_path
    manifest_path = tmp_path / "staticfiles.json"
    manifest_path.write_text(
        json.dumps(
            {
                "paths": {
                    "css/app.css": "css/app.a1.css",
                    "css/app.map": "css/app.a1.map",
                    "css/duplicate.css": "css/app.a1.css",
                }
            }
        ),
        encoding="utf-8",
    )

    command = build_command()
    asset_paths = command._load_manifest_asset_paths(manifest_path)

    assert asset_paths == ["css/app.a1.css", "css/app.a1.map"]


def test_load_manifest_invalid_structure(tmp_path, settings):
    settings.STATIC_ROOT = tmp_path
    manifest_path = tmp_path / "staticfiles.json"
    manifest_path.write_text(json.dumps(["unexpected"]), encoding="utf-8")

    command = build_command()

    with pytest.raises(CommandError):
        command._load_manifest_asset_paths(manifest_path)


def test_apply_skip_patterns():
    command = build_command()
    assets = [
        "js/sentry.123.js",
        "js/other.js",
        "css/app.css",
    ]

    remaining, skipped = command._apply_skip_patterns(assets, ["js/sentry.*", "css/missing.css"])

    assert remaining == ["js/other.js", "css/app.css"]
    assert skipped == {"js/sentry.123.js"}


def test_fetch_asset_head_fallback_to_get(monkeypatch):
    command = build_command()
    responses = [
        _DummyResponse(405, "Method Not Allowed"),
        _DummyResponse(200, "OK"),
    ]

    session = _DummySession(responses)

    result = command._fetch_asset(
        session=session,
        base_url="https://origin.example.com",
        static_prefix="media",
        asset="css/app.css",
        method="head",
        timeout=2,
        retry_count=0,
        retry_backoff=1,
    )

    assert result.status == 200
    assert result.ok


def test_fetch_asset_non_success_head_retries_with_get(monkeypatch):
    command = build_command()
    responses = [
        _DummyResponse(404, "Not Found"),
        _DummyResponse(200, "OK"),
    ]

    session = _DummySession(responses)

    result = command._fetch_asset(
        session=session,
        base_url="https://origin.example.com",
        static_prefix="media",
        asset="css/app.css",
        method="head",
        timeout=2,
        retry_count=0,
        retry_backoff=1,
    )

    assert result.status == 200
    assert result.ok


def test_fetch_asset_request_exception(monkeypatch):
    command = build_command()

    class ErrorSession:
        def request(self, *args, **kwargs):  # pragma: no cover - sanity guard
            raise requests.ConnectionError("boom")

    result = command._fetch_asset(
        session=ErrorSession(),
        base_url="https://origin.example.com",
        static_prefix="media",
        asset="css/app.css",
        method="head",
        timeout=1,
        retry_count=0,
        retry_backoff=1,
    )

    assert result.status is None
    assert not result.ok
    assert "boom" in result.error


def test_fetch_asset_retries_on_timeout(monkeypatch):
    command = build_command()

    class FlakySession:
        def __init__(self):
            self.calls = 0

        def request(self, method, url, timeout, allow_redirects):
            self.calls += 1
            if self.calls == 1:
                raise requests.Timeout("first timeout")
            return _DummyResponse(200, "OK")

        def get(self, url, timeout, allow_redirects):
            return _DummyResponse(200, "OK")

    sleep_calls = []
    monkeypatch.setattr(asset_command.time, "sleep", lambda delay: sleep_calls.append(delay))

    session = FlakySession()

    result = command._fetch_asset(
        session=session,
        base_url="https://cdn.example.com",
        static_prefix="media",
        asset="css/app.css",
        method="head",
        timeout=1,
        retry_count=2,
        retry_backoff=1,
    )

    assert result.status == 200
    assert result.ok
    assert sleep_calls == [1]


def test_fetch_asset_exhausts_retries(monkeypatch):
    command = build_command()

    class TimeoutSession:
        def request(self, method, url, timeout, allow_redirects):
            raise requests.Timeout("still timing out")

        def get(self, url, timeout, allow_redirects):
            raise requests.Timeout("still timing out")

    sleep_calls = []
    monkeypatch.setattr(asset_command.time, "sleep", lambda delay: sleep_calls.append(delay))

    result = command._fetch_asset(
        session=TimeoutSession(),
        base_url="https://cdn.example.com",
        static_prefix="media",
        asset="css/app.css",
        method="head",
        timeout=1,
        retry_count=2,
        retry_backoff=1,
    )

    assert result.status is None
    assert not result.ok
    assert "still timing out" in result.error
    assert sleep_calls == [1, 2]


def test_fetch_asset_redirect(monkeypatch):
    command = build_command()
    responses = [_DummyResponse(302, "Found", headers={"Location": "https://cdn.example.com/media/css/app.css"})]

    session = _DummySession(responses)

    result = command._fetch_asset(
        session=session,
        base_url="https://cdn.example.com",
        static_prefix="media",
        asset="css/app.css",
        method="get",
        timeout=1,
        retry_count=0,
        retry_backoff=1,
    )

    assert result.status == 302
    assert not result.ok
    assert result.error and "Redirected" in result.error


def test_check_host_returns_sorted_results(monkeypatch):
    command = build_command()

    def fake_fetch(self, session, base_url, static_prefix, asset, method, timeout, retry_count, retry_backoff):
        status = 200 if asset.endswith("ok.css") else 404
        return CheckResult(asset_path=asset, url=f"{base_url}/{asset}", status=status, error=None if status == 200 else "Not Found")

    command._fetch_asset = MethodType(fake_fetch, command)

    results = command._check_host(
        base_url="https://origin.example.com",
        static_prefix="media",
        asset_paths=["b.css", "a.ok.css", "c.css"],
        method="head",
        timeout=1,
        max_workers=4,
        retry_count=0,
        retry_backoff=1,
    )

    assert [result.asset_path for result in results] == ["a.ok.css", "b.css", "c.css"]


def test_handle_reports_failures(monkeypatch, tmp_path, settings, capsys):
    settings.STATIC_ROOT = tmp_path
    settings.STATIC_URL = "/media/"

    manifest_path = tmp_path / "staticfiles.json"
    manifest_path.write_text(
        json.dumps(
            {
                "paths": {
                    "css/app.css": "css/app.a1.css",
                    "js/app.js": "js/app.b2.js",
                }
            }
        ),
        encoding="utf-8",
    )

    origin_failures = [
        CheckResult(
            asset_path="css/app.a1.css",
            url="https://origin.example.com/media/css/app.a1.css",
            status=404,
            error="Not Found",
        ),
        CheckResult(
            asset_path="js/app.b2.js",
            url="https://origin.example.com/media/js/app.b2.js",
            status=None,
            error="Timeout",
        ),
    ]
    cdn_results = [
        CheckResult(
            asset_path="css/app.a1.css",
            url="https://origin.example.com/media/css/app.a1.css",
            status=200,
            error=None,
        ),
        CheckResult(
            asset_path="js/app.b2.js",
            url="https://cdn.example.com/media/js/app.b2.js",
            status=503,
            error="Service Unavailable",
        ),
    ]

    sequence = [origin_failures, cdn_results]

    def fake_check_host(self, **kwargs):
        return sequence.pop(0)

    monkeypatch.setattr(Command, "_check_host", fake_check_host)

    command = build_command()

    with pytest.raises(CommandError) as excinfo:
        command.handle(
            origin_host="https://origin.example.com",
            cdn_host="https://cdn.example.com",
            manifest_path=str(manifest_path),
        )

    assert "Asset availability check detected 3 failures" in str(excinfo.value)

    captured = capsys.readouterr()
    err_output = captured.err.splitlines()

    assert any("https://origin.example.com/media/css/app.a1.css" in line for line in err_output)
    assert any("HTTP 404" in line for line in err_output)
    assert any("Timeout" in line for line in err_output)
    assert any("https://cdn.example.com/media/js/app.b2.js" in line for line in err_output)
    assert any("HTTP 503" in line for line in err_output)


def test_handle_respects_skip_patterns(monkeypatch, tmp_path, settings, capsys):
    settings.STATIC_ROOT = tmp_path
    settings.STATIC_URL = "/media/"

    manifest_path = tmp_path / "staticfiles.json"
    manifest_path.write_text(
        json.dumps(
            {
                "paths": {
                    "js/sentry.js": "js/sentry.abc123.js",
                    "css/app.css": "css/app.123.css",
                }
            }
        ),
        encoding="utf-8",
    )

    ok_result = CheckResult(
        asset_path="css/app.123.css",
        url="https://origin.example.com/media/css/app.123.css",
        status=200,
    )

    captured_calls = []

    def fake_check_host(self, **kwargs):
        captured_calls.append(kwargs["asset_paths"])
        return [ok_result]

    monkeypatch.setattr(Command, "_check_host", fake_check_host)

    command = build_command()

    command.handle(
        origin_host="https://origin.example.com",
        cdn_host="https://cdn.example.com",
        manifest_path=str(manifest_path),
        skip_pattern=["js/sentry.*"],
    )

    stdout = capsys.readouterr().out
    assert "Skipping 1 asset(s) due to skip-patterns" in stdout
    assert all(len(call) == 1 and call[0] == "css/app.123.css" for call in captured_calls)


def test_handle_success(monkeypatch, tmp_path, settings):
    settings.STATIC_ROOT = tmp_path
    settings.STATIC_URL = "/media/"

    manifest_path = tmp_path / "staticfiles.json"
    manifest_path.write_text(
        json.dumps(
            {
                "paths": {
                    "css/app.css": "css/app.a1.css",
                    "js/app.js": "js/app.b2.js",
                }
            }
        ),
        encoding="utf-8",
    )

    ok_results = [
        CheckResult(
            asset_path="css/app.a1.css",
            url="https://origin.example.com/media/css/app.a1.css",
            status=200,
        ),
        CheckResult(
            asset_path="js/app.b2.js",
            url="https://origin.example.com/media/js/app.b2.js",
            status=200,
        ),
    ]

    sequence = [ok_results, ok_results]

    def fake_check_host(self, **kwargs):
        return sequence.pop(0)

    monkeypatch.setattr(Command, "_check_host", fake_check_host)

    command = build_command()

    # Should not raise.
    command.handle(
        origin_host="https://origin.example.com",
        cdn_host="https://cdn.example.com",
        manifest_path=str(manifest_path),
    )


class _DummyResponse:
    def __init__(self, status_code, reason, headers=None):
        self.status_code = status_code
        self.reason = reason
        self.headers = headers or {}


class _DummySession:
    def __init__(self, responses):
        self._responses = list(responses)

    def request(self, method, url, timeout, allow_redirects):
        return self._responses.pop(0)

    def get(self, url, timeout, allow_redirects):
        return self._responses.pop(0)
