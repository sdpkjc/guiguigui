from __future__ import annotations

import time
from typing import Any

from ..core.errors import BackendCapabilityError
from ..core.types import DisplayInfo, Key, MouseButton, Point, Rect, Size, WindowInfo, WindowState
from .base import Backend

try:
    import Quartz
    from Cocoa import (
        NSApplicationActivationPolicyRegular,
        NSPasteboard,
        NSScreen,
        NSStringPboardType,
        NSWorkspace,
    )
    from Quartz import (
        CGDisplayBounds,
        CGEventCreate,
        CGEventCreateKeyboardEvent,
        CGEventCreateMouseEvent,
        CGEventGetLocation,
        CGEventPost,
        CGMainDisplayID,
        CGWindowListCopyWindowInfo,
        kCGEventLeftMouseDown,
        kCGEventLeftMouseUp,
        kCGEventMouseMoved,
        kCGEventOtherMouseDown,
        kCGEventOtherMouseUp,
        kCGEventRightMouseDown,
        kCGEventRightMouseUp,
        kCGEventScrollWheel,
        kCGHIDEventTap,
        kCGMouseButtonCenter,
        kCGMouseButtonLeft,
        kCGMouseButtonRight,
        kCGNullWindowID,
        kCGWindowListExcludeDesktopElements,
        kCGWindowListOptionOnScreenOnly,
    )
except ImportError as e:
    raise ImportError(
        "PyObjC is required for macOS backend. Install with: pip install pyobjc-core pyobjc-framework-Quartz pyobjc-framework-Cocoa"
    ) from e


class MacOSBackend(Backend):
    def __init__(self) -> None:
        self._key_code_map = self._build_key_code_map()
        self._reverse_key_map = {v: k for k, v in self._key_code_map.items()}

    def _build_key_code_map(self) -> dict[str, int]:
        return {
            "a": 0x00,
            "b": 0x0B,
            "c": 0x08,
            "d": 0x02,
            "e": 0x0E,
            "f": 0x03,
            "g": 0x05,
            "h": 0x04,
            "i": 0x22,
            "j": 0x26,
            "k": 0x28,
            "l": 0x25,
            "m": 0x2E,
            "n": 0x2D,
            "o": 0x1F,
            "p": 0x23,
            "q": 0x0C,
            "r": 0x0F,
            "s": 0x01,
            "t": 0x11,
            "u": 0x20,
            "v": 0x09,
            "w": 0x0D,
            "x": 0x07,
            "y": 0x10,
            "z": 0x06,
            "0": 0x1D,
            "1": 0x12,
            "2": 0x13,
            "3": 0x14,
            "4": 0x15,
            "5": 0x17,
            "6": 0x16,
            "7": 0x1A,
            "8": 0x1C,
            "9": 0x19,
            "enter": 0x24,
            "return": 0x24,
            "tab": 0x30,
            "space": 0x31,
            "backspace": 0x33,
            "delete": 0x75,
            "esc": 0x35,
            "escape": 0x35,
            "shift": 0x38,
            "ctrl": 0x3B,
            "control": 0x3B,
            "alt": 0x3A,
            "option": 0x3A,
            "cmd": 0x37,
            "command": 0x37,
            "meta": 0x37,
            "left": 0x7B,
            "right": 0x7C,
            "up": 0x7E,
            "down": 0x7D,
            "home": 0x73,
            "end": 0x77,
            "pageup": 0x74,
            "pagedown": 0x79,
            "f1": 0x7A,
            "f2": 0x78,
            "f3": 0x63,
            "f4": 0x76,
            "f5": 0x60,
            "f6": 0x61,
            "f7": 0x62,
            "f8": 0x64,
            "f9": 0x65,
            "f10": 0x6D,
            "f11": 0x67,
            "f12": 0x6F,
            "f13": 0x69,
            "f14": 0x6B,
            "f15": 0x71,
            "capslock": 0x39,
        }

    def _get_key_code(self, key: Key | str) -> int:
        if isinstance(key, Key):
            key = key.value
        key = key.lower()
        if key in self._key_code_map:
            return self._key_code_map[key]
        raise ValueError(f"Unknown key: {key}")

    def mouse_position(self) -> Point:
        event = CGEventCreate(None)
        loc = CGEventGetLocation(event)
        return Point(int(loc.x), int(loc.y))

    def mouse_move_to(self, x: int, y: int) -> None:
        event = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (x, y), 0)
        CGEventPost(kCGHIDEventTap, event)

    def mouse_move_rel(self, dx: int, dy: int) -> None:
        current = self.mouse_position()
        self.mouse_move_to(current.x + dx, current.y + dy)

    def mouse_press(self, button: MouseButton) -> None:
        pos = self.mouse_position()
        if button == MouseButton.LEFT:
            event = CGEventCreateMouseEvent(
                None, kCGEventLeftMouseDown, (pos.x, pos.y), kCGMouseButtonLeft
            )
        elif button == MouseButton.RIGHT:
            event = CGEventCreateMouseEvent(
                None, kCGEventRightMouseDown, (pos.x, pos.y), kCGMouseButtonRight
            )
        elif button == MouseButton.MIDDLE:
            event = CGEventCreateMouseEvent(
                None, kCGEventOtherMouseDown, (pos.x, pos.y), kCGMouseButtonCenter
            )
        else:
            raise ValueError(f"Unsupported button: {button}")
        CGEventPost(kCGHIDEventTap, event)

    def mouse_release(self, button: MouseButton) -> None:
        pos = self.mouse_position()
        if button == MouseButton.LEFT:
            event = CGEventCreateMouseEvent(
                None, kCGEventLeftMouseUp, (pos.x, pos.y), kCGMouseButtonLeft
            )
        elif button == MouseButton.RIGHT:
            event = CGEventCreateMouseEvent(
                None, kCGEventRightMouseUp, (pos.x, pos.y), kCGMouseButtonRight
            )
        elif button == MouseButton.MIDDLE:
            event = CGEventCreateMouseEvent(
                None, kCGEventOtherMouseUp, (pos.x, pos.y), kCGMouseButtonCenter
            )
        else:
            raise ValueError(f"Unsupported button: {button}")
        CGEventPost(kCGHIDEventTap, event)

    def mouse_scroll(self, dx: int, dy: int) -> None:
        event = CGEventCreateMouseEvent(None, kCGEventScrollWheel, (0, 0), 0)
        Quartz.CGEventSetIntegerValueField(event, Quartz.kCGScrollWheelEventDeltaAxis1, dy)
        Quartz.CGEventSetIntegerValueField(event, Quartz.kCGScrollWheelEventDeltaAxis2, dx)
        CGEventPost(kCGHIDEventTap, event)

    def mouse_is_pressed(self, button: MouseButton) -> bool:
        import Quartz

        buttons = Quartz.CGEventSourceButtonState(
            Quartz.kCGEventSourceStateHIDSystemState, button.value
        )
        return bool(buttons)

    def key_press(self, key: Key | str) -> None:
        key_code = self._get_key_code(key)
        event = CGEventCreateKeyboardEvent(None, key_code, True)
        CGEventPost(kCGHIDEventTap, event)

    def key_release(self, key: Key | str) -> None:
        key_code = self._get_key_code(key)
        event = CGEventCreateKeyboardEvent(None, key_code, False)
        CGEventPost(kCGHIDEventTap, event)

    def key_is_pressed(self, key: Key | str) -> bool:
        return False

    def key_type_unicode(self, text: str) -> None:
        for char in text:
            if char.lower() in self._key_code_map:
                key_code = self._key_code_map[char.lower()]
                down_event = CGEventCreateKeyboardEvent(None, key_code, True)
                up_event = CGEventCreateKeyboardEvent(None, key_code, False)

                if char.isupper():
                    shift_code = self._key_code_map["shift"]
                    shift_down = CGEventCreateKeyboardEvent(None, shift_code, True)
                    CGEventPost(kCGHIDEventTap, shift_down)
                    time.sleep(0.01)

                CGEventPost(kCGHIDEventTap, down_event)
                time.sleep(0.01)
                CGEventPost(kCGHIDEventTap, up_event)

                if char.isupper():
                    shift_up = CGEventCreateKeyboardEvent(None, shift_code, False)
                    CGEventPost(kCGHIDEventTap, shift_up)
                    time.sleep(0.01)
            else:
                space_code = self._key_code_map["space"]
                down_event = CGEventCreateKeyboardEvent(None, space_code, True)
                up_event = CGEventCreateKeyboardEvent(None, space_code, False)

                from Quartz import CGEventKeyboardSetUnicodeString

                CGEventKeyboardSetUnicodeString(down_event, len(char), char)
                CGEventKeyboardSetUnicodeString(up_event, len(char), char)

                CGEventPost(kCGHIDEventTap, down_event)
                time.sleep(0.01)
                CGEventPost(kCGHIDEventTap, up_event)

    def get_keyboard_layout(self) -> str:
        try:
            # Try to import from Carbon (requires pyobjc-framework-Carbon)
            from Carbon.HIToolbox import (
                TISCopyCurrentKeyboardInputSource,
                TISGetInputSourceProperty,
                kTISPropertyInputSourceID,
            )

            source = TISCopyCurrentKeyboardInputSource()
            if source:
                source_id = TISGetInputSourceProperty(source, kTISPropertyInputSourceID)
                if source_id:
                    return str(source_id)
        except ImportError:
            # Carbon framework not available, return default
            pass

        return "com.apple.keylayout.US"  # Default US layout

    def get_displays(self) -> list[DisplayInfo]:
        displays: list[DisplayInfo] = []
        max_displays = 32
        err, display_list, count = Quartz.CGGetActiveDisplayList(max_displays, None, None)
        if err or not display_list:
            return displays

        for i in range(count):
            display_id = display_list[i]
            bounds = CGDisplayBounds(display_id)

            scale = 1.0
            for screen in NSScreen.screens():
                screen_frame = screen.frame()
                if (
                    abs(screen_frame.origin.x - bounds.origin.x) < 1
                    and abs(screen_frame.origin.y - bounds.origin.y) < 1
                ):
                    scale = screen.backingScaleFactor()
                    break

            is_primary = display_id == CGMainDisplayID()

            refresh_rate = Quartz.CGDisplayModeGetRefreshRate(
                Quartz.CGDisplayCopyDisplayMode(display_id)
            )
            if refresh_rate == 0:
                refresh_rate = 60.0

            phys_width = int(bounds.size.width * scale)
            phys_height = int(bounds.size.height * scale)

            display_info = DisplayInfo(
                id=str(display_id),
                name=f"Display {i + 1}",
                bounds=Rect(
                    int(bounds.origin.x),
                    int(bounds.origin.y),
                    int(bounds.size.width),
                    int(bounds.size.height),
                ),
                work_area=Rect(
                    int(bounds.origin.x),
                    int(bounds.origin.y),
                    int(bounds.size.width),
                    int(bounds.size.height),
                ),
                scale=scale,
                physical_size=Size(phys_width, phys_height),
                refresh_rate=refresh_rate,
                rotation=0,
                is_primary=is_primary,
            )
            displays.append(display_info)

        return displays

    def get_primary_display(self) -> DisplayInfo:
        displays = self.get_displays()
        for display in displays:
            if display.is_primary:
                return display
        if displays:
            return displays[0]
        raise RuntimeError("No displays found")

    def get_virtual_screen_rect(self) -> Rect:
        displays = self.get_displays()
        if not displays:
            return Rect(0, 0, 0, 0)

        min_x = min(d.bounds.x for d in displays)
        min_y = min(d.bounds.y for d in displays)
        max_x = max(d.bounds.x + d.bounds.width for d in displays)
        max_y = max(d.bounds.y + d.bounds.height for d in displays)

        return Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def list_windows(self, visible_only: bool = True) -> list[WindowInfo]:
        options = kCGWindowListOptionOnScreenOnly if visible_only else 0
        options |= kCGWindowListExcludeDesktopElements

        window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
        windows: list[WindowInfo] = []

        if not window_list:
            return windows

        for window in window_list:
            window_dict = dict(window)

            owner_name = window_dict.get("kCGWindowOwnerName", "")
            window_name = window_dict.get("kCGWindowName", "")
            window_number = window_dict.get("kCGWindowNumber", 0)
            owner_pid = window_dict.get("kCGWindowOwnerPID", 0)

            bounds_dict = window_dict.get("kCGWindowBounds", {})
            x = int(bounds_dict.get("X", 0))
            y = int(bounds_dict.get("Y", 0))
            width = int(bounds_dict.get("Width", 0))
            height = int(bounds_dict.get("Height", 0))

            layer = window_dict.get("kCGWindowLayer", 0)
            is_on_screen = window_dict.get("kCGWindowIsOnscreen", False)

            if width == 0 or height == 0:
                continue

            window_info = WindowInfo(
                handle=window_number,
                title=window_name,
                class_name=owner_name,
                pid=owner_pid,
                process_name=owner_name,
                rect=Rect(x, y, width, height),
                client_rect=Rect(x, y, width, height),
                state=WindowState.NORMAL,
                is_visible=is_on_screen and visible_only,
                is_active=False,
                is_always_on_top=layer > 0,
                opacity=window_dict.get("kCGWindowAlpha", 1.0),
            )
            windows.append(window_info)

        return windows

    def get_active_window(self) -> WindowInfo | None:
        workspace = NSWorkspace.sharedWorkspace()
        active_app = workspace.frontmostApplication()

        if not active_app:
            return None

        pid = active_app.processIdentifier()
        windows = self.list_windows(visible_only=True)

        for window in windows:
            if window.pid == pid:
                window.is_active = True
                return window

        return None

    def get_window_at(self, x: int, y: int) -> WindowInfo | None:
        windows = self.list_windows(visible_only=True)
        point = Point(x, y)

        for window in windows:
            if window.rect.contains(point):
                return window

        return None

    def focus_window(self, handle: Any) -> None:
        windows = self.list_windows(visible_only=False)
        target_window = None

        for window in windows:
            if window.handle == handle:
                target_window = window
                break

        if not target_window:
            return

        workspace = NSWorkspace.sharedWorkspace()
        running_apps = workspace.runningApplications()

        for app in running_apps:
            if app.processIdentifier() == target_window.pid:
                app.activateWithOptions_(NSApplicationActivationPolicyRegular)
                break

    def move_window(self, handle: Any, x: int, y: int) -> None:
        raise BackendCapabilityError("move_window", "macOS")

    def resize_window(self, handle: Any, width: int, height: int) -> None:
        raise BackendCapabilityError("resize_window", "macOS")

    def set_window_state(self, handle: Any, state: WindowState) -> None:
        raise BackendCapabilityError("set_window_state", "macOS")

    def get_window_state(self, handle: Any) -> WindowState:
        return WindowState.NORMAL

    def close_window(self, handle: Any) -> None:
        raise BackendCapabilityError("close_window", "macOS")

    def set_window_opacity(self, handle: Any, opacity: float) -> None:
        raise BackendCapabilityError("set_window_opacity", "macOS")

    def set_window_always_on_top(self, handle: Any, enabled: bool) -> None:
        raise BackendCapabilityError("set_window_always_on_top", "macOS")

    def clipboard_get_text(self) -> str:
        pasteboard = NSPasteboard.generalPasteboard()
        text = pasteboard.stringForType_(NSStringPboardType)
        return text if text else ""

    def clipboard_set_text(self, text: str) -> None:
        pasteboard = NSPasteboard.generalPasteboard()
        pasteboard.clearContents()
        pasteboard.setString_forType_(text, NSStringPboardType)

    def clipboard_clear(self) -> None:
        pasteboard = NSPasteboard.generalPasteboard()
        pasteboard.clearContents()

    def clipboard_has_text(self) -> bool:
        pasteboard = NSPasteboard.generalPasteboard()
        return pasteboard.stringForType_(NSStringPboardType) is not None

    def check_permissions(self) -> dict[str, bool]:
        perms = {
            "mouse": True,
            "keyboard": True,
            "window": True,
            "accessibility": self._check_accessibility(),
        }
        return perms

    def _check_accessibility(self) -> bool:
        import Quartz

        return Quartz.AXIsProcessTrusted()
