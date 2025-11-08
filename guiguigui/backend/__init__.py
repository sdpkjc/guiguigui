from __future__ import annotations

import sys

from .base import Backend

_backend: Backend | None = None


def get_backend() -> Backend:
    global _backend
    if _backend is None:
        _backend = _load_backend()
    return _backend


def _load_backend() -> Backend:
    platform = sys.platform

    if platform == "darwin":
        from .macos import MacOSBackend

        return MacOSBackend()

    elif platform == "win32":
        from .win32 import Win32Backend

        return Win32Backend()  # type: ignore[abstract]

    elif platform.startswith("linux"):
        import os

        wayland_display = os.environ.get("WAYLAND_DISPLAY")
        xdg_session_type = os.environ.get("XDG_SESSION_TYPE")

        if wayland_display or xdg_session_type == "wayland":
            try:
                from .wayland import WaylandBackend

                return WaylandBackend()  # type: ignore[abstract]
            except ImportError:
                pass

        from .x11 import X11Backend

        return X11Backend()

    else:
        raise NotImplementedError(f"Platform {platform} is not supported")
