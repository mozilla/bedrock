# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core.cache import caches

import pytest

from bedrock.base.cache import get_from_hybrid_cache, set_in_hybrid_cache

pytestmark = [
    pytest.mark.django_db,
]

local_cache = caches["default"]
db_cache = caches["db"]


@pytest.fixture(autouse=True)
def clear_caches():
    local_cache.clear()
    db_cache.clear()


def test_hybrid_cache_get():
    key = "test_key"
    value = "test_value"

    local_cache.set(
        key,
        value,
        timeout=settings.CACHE_TIME_SHORT,
    )
    db_cache.set(
        key,
        value,
        timeout=settings.CACHE_TIME_SHORT,
    )

    # Test getting from local cache directly
    assert get_from_hybrid_cache(key) == value

    # Test falling back to db cache and populating local cache
    local_cache.clear()
    assert local_cache.get(key) is None
    assert db_cache.get(key) == value

    assert get_from_hybrid_cache(key) == value
    assert local_cache.get(key) == value


def test_hybrid_cache_get_no_values_in_local_or_db_cache():
    key = "test_key"

    assert local_cache.get(key) is None
    assert db_cache.get(key) is None
    assert get_from_hybrid_cache(key) is None


def test_hybrid_cache_get__default_value():
    # Test getting default value when key is not found
    assert (
        get_from_hybrid_cache(
            "non_existent_key",
            default="default_value",
        )
        == "default_value"
    )


def test_hybrid_cache_set():
    key = "test_key"
    value = "test_value"
    set_in_hybrid_cache(key, value)

    assert local_cache.get(key) == value
    assert db_cache.get(key) == value


def test_set_in_hybrid_cache_db_cache_failure(caplog, mocker):
    key = "test_key_db_failure"
    value = "test_value_db_failure"
    timeout = 60

    mocker.patch.object(
        db_cache,
        "set",
        side_effect=Exception("Faked DB cache failure"),
    )

    set_in_hybrid_cache(key, value, timeout)

    assert local_cache.get(key) == value
    assert db_cache.get(key) is None

    assert caplog.records[0].msg == "Could not set value in DB-backed cache: Faked DB cache failure"


def test_set_in_hybrid_cache_default_timeouts(mocker):
    key = "test_key"
    value = "test_value"

    mock_db_set = mocker.patch.object(caches["db"], "set")
    mock_local_set = mocker.patch.object(caches["default"], "set")

    set_in_hybrid_cache(key, value)

    mock_db_set.assert_called_once_with(key, value, timeout=None)
    mock_local_set.assert_called_once_with(key, value, timeout=settings.CACHE_TIME_SHORT)


def test_set_in_hybrid_cache_custom_db_cache_timeout(mocker):
    key = "test_key"
    value = "test_value"
    custom_db_cache_timeout = 120

    mock_db_set = mocker.patch.object(caches["db"], "set")
    mock_local_set = mocker.patch.object(caches["default"], "set")
    set_in_hybrid_cache(key, value, db_cache_timeout=custom_db_cache_timeout)

    mock_db_set.assert_called_once_with(key, value, timeout=custom_db_cache_timeout)
    mock_local_set.assert_called_once_with(key, value, timeout=settings.CACHE_TIME_SHORT)


def test_set_in_hybrid_cache_custom_locmem_cache_timeout(mocker):
    key = "test_key"
    value = "test_value"
    custom_locmem_cache_timeout = 42

    mock_db_set = mocker.patch.object(caches["db"], "set")
    mock_local_set = mocker.patch.object(caches["default"], "set")

    set_in_hybrid_cache(key, value, locmem_cache_timeout=custom_locmem_cache_timeout)

    mock_db_set.assert_called_once_with(key, value, timeout=None)
    mock_local_set.assert_called_once_with(key, value, timeout=custom_locmem_cache_timeout)
