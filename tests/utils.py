# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import functools
import importlib
from collections.abc import Callable
from typing import Any

from django.test import override_settings


def reload_redirects_with_settings(module_path: str, **settings_kwargs):
    """
    Generic decorator that enables dynamic redirect reloading for testing.

    This decorator:
    1. Overrides specified settings using the same pattern as @override_settings
    2. Reloads the specified redirects module to pick up new patterns
    3. Patches the redirects middleware to use the reloaded patterns
    4. Restores original state after the test

    This is needed because Django loads redirects once at startup and doesn't
    reload them when @override_settings is used.

    Args:
        module_path: The module path to reload (e.g., 'bedrock.firefox.redirects')
        **settings_kwargs: Settings to override (e.g., ENABLE_FIREFOX_COM_REDIRECTS=True)

    Usage:
        @reload_redirects_with_settings('bedrock.firefox.redirects', ENABLE_FIREFOX_COM_REDIRECTS=True)
        def test_my_redirect():
            # Your test code here
            pass
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with override_settings(**settings_kwargs):
                original_patterns, original_resolver = _patch_redirects_middleware(module_path)
                try:
                    return func(*args, **kwargs)
                finally:
                    _restore_redirects_middleware(module_path, original_patterns, original_resolver)

        return wrapper

    return decorator


def _patch_redirects_middleware(module_path: str) -> tuple[Any, Any]:
    """
    Patch the redirects middleware to use reloaded patterns from the specified module.

    Args:
        module_path: The module path to reload

    Returns:
        Tuple of (original_patterns, original_resolver) for restoration
    """
    import bedrock.redirects.middleware

    # Import and reload the specified module
    module = importlib.import_module(module_path)
    importlib.reload(module)  # type: ignore

    # Store original state
    original_patterns = module.redirectpatterns  # type: ignore
    original_resolver = bedrock.redirects.middleware.get_resolver

    # Patch the resolver to use the reloaded patterns
    def patched_get_resolver(patterns=None):
        if patterns is None:
            patterns = module.redirectpatterns  # type: ignore
        return original_resolver(patterns)

    bedrock.redirects.middleware.get_resolver = patched_get_resolver

    return original_patterns, original_resolver


def _restore_redirects_middleware(module_path: str, original_patterns: Any, original_resolver: Any) -> None:
    """
    Restore the original redirects middleware state.

    Args:
        module_path: The module path that was reloaded
        original_patterns: The original redirectpatterns to restore
        original_resolver: The original get_resolver function to restore
    """
    import bedrock.redirects.middleware

    # Restore original patterns
    module = importlib.import_module(module_path)
    module.redirectpatterns = original_patterns  # type: ignore

    # Restore original resolver
    bedrock.redirects.middleware.get_resolver = original_resolver
