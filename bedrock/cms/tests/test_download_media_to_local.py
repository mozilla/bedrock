# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from io import StringIO
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.core.management import call_command

import pytest

from bedrock.cms.management.commands import download_media_to_local
from bedrock.cms.models import BedrockImage

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def media_root(settings, tmp_path):
    settings.MEDIA_ROOT = str(tmp_path / "media")
    return tmp_path / "media"


@pytest.fixture(autouse=True)
def pre_generate_renditions():
    with patch.object(BedrockImage, "_pre_generate_expected_renditions", autospec=True) as pre_generate_mock:
        yield pre_generate_mock


@pytest.fixture
def storage_client():
    with patch.object(download_media_to_local.storage.Client, "create_anonymous_client") as create_mock:
        yield create_mock.return_value


@pytest.fixture
def image(pre_generate_renditions):
    image = BedrockImage.objects.create(title="Fox", file="original_images/fox.jpg", width=100, height=100)
    pre_generate_renditions.reset_mock()
    return image


def run(*args):
    out, err = StringIO(), StringIO()
    call_command("download_media_to_local", *args, stdout=out, stderr=err)
    return out.getvalue(), err.getvalue()


def downloaded_blobs(storage_client):
    return [blob_call.args[0] for blob_call in storage_client.bucket.return_value.blob.call_args_list]


def test_refuses_to_run_off_sqlite(storage_client):
    err = StringIO()
    with patch.dict(settings.DATABASES["default"], {"ENGINE": "django.db.backends.postgresql"}):
        with pytest.raises(SystemExit) as exit_info:
            call_command("download_media_to_local", stderr=err)

    assert exit_info.value.code == 1
    assert "only works if you are using sqlite" in err.getvalue()
    assert "django.db.backends.postgresql" in err.getvalue()
    storage_client.bucket.assert_not_called()


def test_refuses_an_unknown_environment(storage_client):
    err = StringIO()
    with pytest.raises(SystemExit) as exit_info:
        call_command("download_media_to_local", environment="qa", stderr=err)

    assert exit_info.value.code == 1
    assert err.getvalue() == "Couldn't determine which bucket you wanted. Got qa\n"
    storage_client.bucket.assert_not_called()


@pytest.mark.parametrize(
    "args, bucket_name",
    [
        ([], "bedrock-nonprod-dev-cms-media"),
        (["--environment", "dev"], "bedrock-nonprod-dev-cms-media"),
        (["--environment", "stage"], "bedrock-nonprod-stage-cms-media"),
        (["--environment", "prod"], "bedrock-prod-prod-cms-media"),
    ],
)
def test_environment_picks_the_bucket(storage_client, args, bucket_name):
    run(*args)
    storage_client.bucket.assert_called_once_with(bucket_name)


def test_downloads_missing_image(storage_client, image, media_root, pre_generate_renditions):
    out, _ = run()

    local_dest = media_root / "original_images" / "fox.jpg"
    assert downloaded_blobs(storage_client) == ["media/cms/original_images/fox.jpg"]
    download = storage_client.bucket.return_value.blob.return_value.download_to_filename
    download.assert_called_once()
    assert Path(download.call_args.args[0]) == local_dest
    assert f"Downloaded media/cms/original_images/fox.jpg from bedrock-nonprod-dev-cms-media to {local_dest}" in out
    pre_generate_renditions.assert_called_once_with(image)
    assert out.endswith("All done.\n")


def test_creates_the_media_dirs(storage_client, image, media_root):
    out, _ = run()

    assert (media_root / "original_images").is_dir()
    assert (media_root / "images").is_dir()
    assert f"setting up: {media_root / 'original_images'}" in out


def test_skips_image_already_downloaded(storage_client, image, media_root, pre_generate_renditions):
    (media_root / "original_images").mkdir(parents=True)
    (media_root / "original_images" / "fox.jpg").write_bytes(b"fox")

    out, _ = run()

    assert downloaded_blobs(storage_client) == []
    pre_generate_renditions.assert_not_called()
    assert f"Skipping: {media_root / 'original_images' / 'fox.jpg'} already exists locally." in out


def test_redownload_replaces_existing_image_and_its_renditions(storage_client, image, media_root, pre_generate_renditions):
    (media_root / "original_images").mkdir(parents=True)
    (media_root / "original_images" / "fox.jpg").write_bytes(b"fox")
    image.renditions.create(filter_spec="width-100", file="images/fox.width-100.jpg", width=100, height=100)
    other_image = BedrockImage.objects.create(title="Panda", file="original_images/panda.jpg", width=100, height=100)
    other_image.renditions.create(filter_spec="width-100", file="images/panda.width-100.jpg", width=100, height=100)
    pre_generate_renditions.reset_mock()

    out, _ = run("--redownload")

    assert out.startswith("Forcing redownload of all files.\n")
    assert sorted(downloaded_blobs(storage_client)) == ["media/cms/original_images/fox.jpg", "media/cms/original_images/panda.jpg"]
    assert not image.renditions.exists()
    assert not other_image.renditions.exists()
    assert pre_generate_renditions.call_count == 2


def test_no_images_means_nothing_to_download(storage_client, media_root):
    out, _ = run()

    assert downloaded_blobs(storage_client) == []
    assert out == "All done.\n"
