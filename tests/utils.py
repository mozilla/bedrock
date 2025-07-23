# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import functools
import importlib
from collections.abc import Callable
from typing import Any

from django.test import override_settings


def reload_redirects_with_settings(redirects_module_path: str, middleware_module_path: str, **settings_kwargs):
    """
    Generic decorator that enables dynamic redirect reloading for testing.

    This decorator:
    1. Stores the original setting values before any changes
    2. Overrides specified settings using the same pattern as @override_settings
    3. Reloads the specified redirects module to pick up new patterns
    4. Patches the specified middleware module to use the reloaded patterns
    5. Restores original settings and reloads module again after the test

    This is needed because Django loads redirects once at startup and doesn't
    reload them when @override_settings is used.

    Args:
        redirects_module_path: The redirects module path to reload
        middleware_module_path: The middleware module path to patch
        **settings_kwargs: Settings to override

    Usage:
        @reload_redirects_with_settings(
            'bedrock.firefox.redirects',
            'bedrock.redirects.middleware',
            ENABLE_FIREFOX_COM_REDIRECTS=True
        )
        def test_my_redirect():
            # Your test code here
            pass
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            from django.conf import settings

            original_settings = {}
            for setting_name in settings_kwargs.keys():
                original_settings[setting_name] = getattr(settings, setting_name, None)

            with override_settings(**settings_kwargs):
                original_get_resolver = _reload_module_and_patch_middleware(redirects_module_path, middleware_module_path)
                try:
                    return func(*args, **kwargs)
                finally:
                    restore_settings = {name: value for name, value in original_settings.items()}
                    with override_settings(**restore_settings):
                        _reload_module_and_patch_middleware(redirects_module_path, middleware_module_path)
                    middleware_module = importlib.import_module(middleware_module_path)
                    middleware_module.get_resolver = original_get_resolver

        return wrapper

    return decorator


def _reload_module_and_patch_middleware(redirects_module_path: str, middleware_module_path: str) -> Any:
    """
    Import, reload the specified module, and patch the redirects middleware.

    Args:
        redirects_module_path: The redirects module path to reload
        middleware_module_path: The middleware module path to patch

    Returns:
        The original get_resolver function for restoration
    """
    middleware_module = importlib.import_module(middleware_module_path)

    redirects_module = importlib.import_module(redirects_module_path)
    importlib.reload(redirects_module)  # type: ignore
    original_get_resolver = middleware_module.get_resolver

    def patched_get_resolver(patterns=None):
        if patterns is None:
            patterns = redirects_module.redirectpatterns  # type: ignore
        return original_get_resolver(patterns)

    middleware_module.get_resolver = patched_get_resolver

    return original_get_resolver


def enable_fxc_redirects():
    """
    Convenience decorator for Firefox.com redirect testing.

    This is a wrapper around reload_redirects_with_settings that enables
    Firefox.com redirects for the duration of the test regardless of the
    ENABLE_FIREFOX_COM_REDIRECTS environment variable.

    Usage:
        @enable_fxc_redirects()
        def test_my_redirect():
            # Your test code here
            pass
    """
    return reload_redirects_with_settings("bedrock.firefox.redirects", "bedrock.redirects.middleware", ENABLE_FIREFOX_COM_REDIRECTS=True)
