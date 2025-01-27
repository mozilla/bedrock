# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core.cache import caches

import pytest

from bedrock.cms.models import SimpleKVStore
from bedrock.cms.utils import get_from_cache_wrapped_kv_store, set_in_cached_wrapped_kv_store

pytestmark = [
    pytest.mark.django_db,
]

local_cache = caches["default"]


@pytest.fixture(autouse=True)
def clear_caches():
    local_cache.clear()


def _set_in_db(key, value):
    try:
        store = SimpleKVStore.objects.get(key=key)
    except SimpleKVStore.DoesNotExist:
        store = SimpleKVStore(key=key)
    store.value = value
    store.save()


def _get_from_db(key):
    try:
        store = SimpleKVStore.objects.get(key=key)
        return store.value
    except SimpleKVStore.DoesNotExist:
        return None


def test_hybrid_cache_get():
    key = "test_key"
    value = "test_value"

    local_cache.set(
        key,
        value,
        timeout=settings.CACHE_TIME_SHORT,
    )
    _set_in_db(
        key,
        value,
    )

    # Test getting from local cache directly
    assert get_from_cache_wrapped_kv_store(key) == value

    # Test falling back to db cache and populating local cache
    local_cache.clear()
    assert local_cache.get(key) is None
    assert _get_from_db(key) == value

    assert get_from_cache_wrapped_kv_store(key) == value
    assert local_cache.get(key) == value


def test_hybrid_cache_get_no_values_in_local_or_db_cache():
    key = "test_key"

    assert local_cache.get(key) is None
    assert _get_from_db(key) is None
    assert get_from_cache_wrapped_kv_store(key) is None


def test_hybrid_cache_get__default_value():
    # Test getting default value when key is not found
    assert (
        get_from_cache_wrapped_kv_store(
            "non_existent_key",
            default="default_value",
        )
        == "default_value"
    )


def test_hybrid_cache_set():
    key = "test_key"
    value = "test_value"
    set_in_cached_wrapped_kv_store(key, value)

    assert local_cache.get(key) == value
    assert _get_from_db(key) == value


def test_set_in_cached_wrapped_kv_store_db_cache_failure(caplog, mocker):
    key = "test_key_db_failure"
    value = "test_value_db_failure"

    mocker.patch(
        "bedrock.cms.utils._set_in_db_kv_store",
        side_effect=Exception("Faked DB cache failure"),
    )

    set_in_cached_wrapped_kv_store(key, value)

    assert local_cache.get(key) == value
    assert _get_from_db(key) is None

    assert caplog.records[0].msg == "Could not set value in DB-backed cache: Faked DB cache failure"


def test_type_conversion_of_set_during_db_storage():
    input = set(["hello", "world", 123])
    assert isinstance(input, set)

    set_in_cached_wrapped_kv_store("test-key", input)
    output = get_from_cache_wrapped_kv_store("test-key")
    assert isinstance(output, list)

    # also be sure the locmem version was turned into a list, too
    assert isinstance(local_cache.get("test-key"), list)

    assert set(output) == input
