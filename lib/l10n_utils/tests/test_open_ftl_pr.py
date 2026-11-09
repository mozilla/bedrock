# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import Mock

from django.test.utils import override_settings

from lib.l10n_utils.management.commands.open_ftl_pr import Command


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _files(root):
    return sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())


@override_settings(FLUENT_REPO_AUTH="")
def test_sync_dirs_purges_removed_files_but_keeps_locales(tmp_path):
    source = tmp_path / "bedrock"
    target = tmp_path / "www-l10n"

    # bedrock's l10n folder
    _write(source / "l10n-pontoon.toml", "new pontoon config")
    _write(source / "configs" / "pontoon.toml", "pontoon")
    _write(source / "en" / "brands.ftl", "updated brands")
    _write(source / "en" / "firefox" / "new.ftl", "new file")
    _write(source / "en-US" / "mozorg" / "home.ftl", "home")

    # l10n team repo, with obsolete files and locale folders
    _write(target / ".github" / "workflows" / "ci.yml", "ci")
    _write(target / "README.md", "readme")
    _write(target / "l10n-pontoon.toml", "old pontoon config")
    _write(target / "configs" / "pontoon.toml", "pontoon")
    _write(target / "configs" / "obsolete.toml", "obsolete")
    _write(target / "en" / "brands.ftl", "old brands")
    _write(target / "en" / "404-locale.ftl", "obsolete")
    _write(target / "en" / "firefox" / "features" / "index.ftl", "obsolete")
    _write(target / "en-US" / "mozorg" / "home.ftl", "home")
    _write(target / "en-US" / "firefox" / "whatsnew" / "whatsnew-fx80.ftl", "obsolete")
    _write(target / "fr" / "brands.ftl", "marques")
    _write(target / "fr" / "404-locale.ftl", "translated")

    cmd = Command()
    cmd.l10n_repo = Mock(path=target)
    with override_settings(FLUENT_LOCAL_PATH=source):
        cmd.sync_dirs()

    assert _files(target) == [
        ".github/workflows/ci.yml",
        "README.md",
        "configs/pontoon.toml",
        "en-US/mozorg/home.ftl",
        "en/brands.ftl",
        "en/firefox/new.ftl",
        "fr/404-locale.ftl",
        "fr/brands.ftl",
        "l10n-pontoon.toml",
    ]
    assert not (target / "en" / "firefox" / "features").exists()
    assert not (target / "en-US" / "firefox").exists()
    assert (target / "en" / "brands.ftl").read_text() == "updated brands"
    assert (target / "l10n-pontoon.toml").read_text() == "new pontoon config"
    assert (target / "fr" / "brands.ftl").read_text() == "marques"
