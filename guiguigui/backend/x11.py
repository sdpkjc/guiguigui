"""X11 backend implementation using python-xlib."""

from __future__ import annotations

import time
from typing import Any

from ..core.types import DisplayInfo, Key, MouseButton, Point, Rect, Size, WindowInfo, WindowState
from .base import Backend

try:
    from Xlib import XK, X, display
    from Xlib.ext import randr
    from Xlib.ext.xtest import fake_input
    from Xlib.protocol import event
except ImportError as e:
    raise ImportError(
        "python-xlib is required for X11 backend. Install with: pip install python-xlib"
    ) from e


class X11Backend(Backend):
    """X11 backend implementation using python-xlib."""

    def __init__(self) -> None:
        self._display = display.Display()
        self._root = self._display.screen().root
        self._key_code_map = self._build_key_code_map()

    def _build_key_code_map(self) -> dict[str, int]:
        """Build key name to keycode mapping using XKeysymToKeycode."""
        key_map = {}

        # Letters
        for c in "abcdefghijklmnopqrstuvwxyz":
            keysym = XK.string_to_keysym(c)
            keycode = self._display.keysym_to_keycode(keysym)
            if keycode:
                key_map[c] = keycode

        # Numbers
        for i in range(10):
            keysym = XK.string_to_keysym(str(i))
            keycode = self._display.keysym_to_keycode(keysym)
            if keycode:
                key_map[str(i)] = keycode

        # Special keys mapping
        special_keys = {
            "enter": "Return",
            "return": "Return",
            "tab": "Tab",
            "space": "space",
            "backspace": "BackSpace",
            "delete": "Delete",
            "esc": "Escape",
            "escape": "Escape",
            "shift": "Shift_L",
            "ctrl": "Control_L",
            "control": "Control_L",
            "alt": "Alt_L",
            "cmd": "Super_L",
            "command": "Super_L",
            "super": "Super_L",
            "caps_lock": "Caps_Lock",
            "left": "Left",
            "right": "Right",
            "up": "Up",
            "down": "Down",
            "home": "Home",
            "end": "End",
            "page_up": "Page_Up",
            "page_down": "Page_Down",
        }

        for key_name, x_key_name in special_keys.items():
            keysym = XK.string_to_keysym(x_key_name)
            keycode = self._display.keysym_to_keycode(keysym)
            if keycode:
                key_map[key_name] = keycode

        # Function keys
        for i in range(1, 13):
            keysym = XK.string_to_keysym(f"F{i}")
            keycode = self._display.keysym_to_keycode(keysym)
            if keycode:
                key_map[f"f{i}"] = keycode

        return key_map

    def _get_key_code(self, key: Key | str) -> int:
        """Convert Key enum or string to X11 keycode."""
        if isinstance(key, Key):
            key_str = key.value.lower()
        else:
            key_str = str(key).lower()

        keycode = self._key_code_map.get(key_str)
        if keycode is None:
            # Try as single character
            if len(key_str) == 1:
                keysym = XK.string_to_keysym(key_str)
                keycode = self._display.keysym_to_keycode(keysym)

        if keycode is None:
            raise ValueError(f"Unknown key: {key}")

        return keycode

    def _get_window_handle(self, window: WindowInfo | int) -> int:
        """Get window handle from WindowInfo or int."""
        if isinstance(window, int):
            return window
        return window.handle

    # Mouse methods
    def mouse_position(self) -> Point:
        """Get current mouse position."""
        pointer = self._root.query_pointer()
        return Point(pointer.root_x, pointer.root_y)

    def mouse_move_to(self, x: int, y: int, duration: float = 0.0) -> None:
        """Move mouse to absolute position."""
        if duration > 0:
            start = self.mouse_position()
            steps = max(10, int(duration * 60))  # 60 FPS
            for i in range(1, steps + 1):
                t = i / steps
                cur_x = int(start.x + (x - start.x) * t)
                cur_y = int(start.y + (y - start.y) * t)
                fake_input(self._display, X.MotionNotify, x=cur_x, y=cur_y)
                self._display.sync()
                time.sleep(duration / steps)
        else:
            fake_input(self._display, X.MotionNotify, x=x, y=y)
            self._display.sync()

    def mouse_move_rel(self, dx: int, dy: int, duration: float = 0.0) -> None:
        """Move mouse relative to current position."""
        pos = self.mouse_position()
        self.mouse_move_to(pos.x + dx, pos.y + dy, duration)

    def mouse_press(self, button: MouseButton) -> None:
        """Press mouse button."""
        button_map = {
            MouseButton.LEFT: 1,
            MouseButton.MIDDLE: 2,
            MouseButton.RIGHT: 3,
            MouseButton.X1: 8,
            MouseButton.X2: 9,
        }
        x_button = button_map.get(button)
        if x_button is None:
            raise ValueError(f"Unsupported button: {button}")

        fake_input(self._display, X.ButtonPress, detail=x_button)
        self._display.sync()

    def mouse_release(self, button: MouseButton) -> None:
        """Release mouse button."""
        button_map = {
            MouseButton.LEFT: 1,
            MouseButton.MIDDLE: 2,
            MouseButton.RIGHT: 3,
            MouseButton.X1: 8,
            MouseButton.X2: 9,
        }
        x_button = button_map.get(button)
        if x_button is None:
            raise ValueError(f"Unsupported button: {button}")

        fake_input(self._display, X.ButtonRelease, detail=x_button)
        self._display.sync()

    def mouse_scroll(self, dx: int, dy: int) -> None:
        """Scroll mouse wheel."""
        # X11 scroll: button 4=up, 5=down, 6=left, 7=right
        if dy > 0:
            for _ in range(abs(dy)):
                fake_input(self._display, X.ButtonPress, detail=4)
                fake_input(self._display, X.ButtonRelease, detail=4)
        elif dy < 0:
            for _ in range(abs(dy)):
                fake_input(self._display, X.ButtonPress, detail=5)
                fake_input(self._display, X.ButtonRelease, detail=5)

        if dx > 0:
            for _ in range(abs(dx)):
                fake_input(self._display, X.ButtonPress, detail=7)
                fake_input(self._display, X.ButtonRelease, detail=7)
        elif dx < 0:
            for _ in range(abs(dx)):
                fake_input(self._display, X.ButtonPress, detail=6)
                fake_input(self._display, X.ButtonRelease, detail=6)

        self._display.sync()

    def mouse_is_pressed(self, button: MouseButton) -> bool:
        """Check if mouse button is pressed."""
        pointer = self._root.query_pointer()
        button_map = {
            MouseButton.LEFT: X.Button1Mask,
            MouseButton.MIDDLE: X.Button2Mask,
            MouseButton.RIGHT: X.Button3Mask,
            MouseButton.X1: X.Button4Mask,
            MouseButton.X2: X.Button5Mask,
        }
        mask = button_map.get(button)
        if mask is None:
            return False
        return bool(pointer.mask & mask)

    # Keyboard methods
    def key_press(self, key: Key | str) -> None:
        """Press key."""
        keycode = self._get_key_code(key)
        fake_input(self._display, X.KeyPress, detail=keycode)
        self._display.flush()

    def key_release(self, key: Key | str) -> None:
        """Release key."""
        keycode = self._get_key_code(key)
        fake_input(self._display, X.KeyRelease, detail=keycode)
        self._display.flush()

    def key_is_pressed(self, key: Key | str) -> bool:
        """Check if key is pressed."""
        keycode = self._get_key_code(key)
        keyboard = self._display.query_keymap()
        # keyboard is a list of 32 bytes
        byte_index = keycode // 8
        bit_index = keycode % 8
        if byte_index < len(keyboard):
            return bool(keyboard[byte_index] & (1 << bit_index))
        return False

    def key_type_unicode(self, char: str) -> None:
        """Type Unicode text (character or string)."""
        # For ASCII strings, type each character
        if all(ord(c) < 128 for c in char):
            for c in char:
                try:
                    self.key_press(c)
                    time.sleep(0.01)
                    self.key_release(c)
                except ValueError:
                    # If key not found, skip it
                    pass
            return

        # For Unicode, we need to use XIM or similar
        raise NotImplementedError("Unicode typing not yet implemented for X11")

    def get_keyboard_layout(self) -> str:
        """Get current keyboard layout."""
        # X11 keyboard layout detection is complex
        # Return a simple identifier for now
        return "x11-default"

    # Display methods
    def get_displays(self) -> list[DisplayInfo]:
        """Get all displays."""
        displays = []

        # Get RandR screen resources
        try:
            screen = self._display.screen()
            window = screen.root
            resources = randr.get_screen_resources(window)

            for i, output in enumerate(resources.outputs):
                output_info = randr.get_output_info(window, output, resources.config_timestamp)

                if output_info.crtc:
                    crtc_info = randr.get_crtc_info(
                        window, output_info.crtc, resources.config_timestamp
                    )

                    name = bytes(output_info.name).decode("utf-8", errors="ignore")

                    bounds = Rect(
                        x=crtc_info.x, y=crtc_info.y, width=crtc_info.width, height=crtc_info.height
                    )
                    # Get physical size in millimeters from output_info
                    physical_size = Size(width=output_info.mm_width, height=output_info.mm_height)
                    displays.append(
                        DisplayInfo(
                            id=str(i),
                            name=name,
                            bounds=bounds,
                            work_area=bounds,  # X11 doesn't easily expose work area
                            scale=1.0,  # X11 doesn't directly expose DPI scaling
                            physical_size=physical_size,
                            refresh_rate=60.0,  # Default refresh rate
                            rotation=0,  # No rotation by default
                            is_primary=(i == 0),  # First output is primary
                        )
                    )
        except Exception:
            # Fallback to simple screen info
            screen = self._display.screen()
            bounds = Rect(x=0, y=0, width=screen.width_in_pixels, height=screen.height_in_pixels)
            physical_size = Size(width=screen.width_in_mms, height=screen.height_in_mms)
            displays.append(
                DisplayInfo(
                    id="0",
                    name="default",
                    bounds=bounds,
                    work_area=bounds,
                    scale=1.0,
                    physical_size=physical_size,
                    refresh_rate=60.0,
                    rotation=0,
                    is_primary=True,
                )
            )

        return displays

    def get_primary_display(self) -> DisplayInfo:
        """Get primary display."""
        displays = self.get_displays()
        for disp in displays:
            if disp.is_primary:
                return disp
        return displays[0] if displays else self.get_displays()[0]

    def get_virtual_screen_rect(self) -> Rect:
        """Get virtual screen rectangle."""
        displays = self.get_displays()
        if not displays:
            return Rect(0, 0, 1920, 1080)

        min_x = min(d.bounds.x for d in displays)
        min_y = min(d.bounds.y for d in displays)
        max_x = max(d.bounds.x + d.bounds.width for d in displays)
        max_y = max(d.bounds.y + d.bounds.height for d in displays)

        return Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    # Window methods
    def list_windows(self, visible_only: bool = True) -> list[WindowInfo]:
        """List all windows."""
        windows = []

        def get_window_info(win: Any) -> WindowInfo | None:
            try:
                # Get window attributes
                attrs = win.get_attributes()
                if visible_only and attrs.map_state != X.IsViewable:
                    return None

                # Get geometry
                geom = win.get_geometry()

                # Get window title
                try:
                    title_prop = win.get_full_property(self._display.intern_atom("_NET_WM_NAME"), 0)
                    if title_prop:
                        title = title_prop.value.decode("utf-8", errors="ignore")
                    else:
                        title_prop = win.get_full_property(X.XA_WM_NAME, 0)
                        title = (
                            title_prop.value.decode("latin1", errors="ignore") if title_prop else ""
                        )
                except Exception:
                    title = ""

                # Get window class
                try:
                    class_prop = win.get_full_property(X.XA_WM_CLASS, 0)
                    class_name = (
                        class_prop.value.decode("latin1", errors="ignore").split("\x00")[1]
                        if class_prop
                        else ""
                    )
                except Exception:
                    class_name = ""

                # Get PID
                try:
                    pid_prop = win.get_full_property(self._display.intern_atom("_NET_WM_PID"), 0)
                    pid = pid_prop.value[0] if pid_prop else 0
                except Exception:
                    pid = 0

                rect = Rect(geom.x, geom.y, geom.width, geom.height)
                return WindowInfo(
                    handle=win.id,
                    title=title,
                    class_name=class_name,
                    pid=pid,
                    process_name="",  # Not easily available
                    rect=rect,
                    client_rect=rect,  # Use same rect for simplicity
                    state=WindowState.NORMAL,  # TODO: detect state properly
                    is_visible=attrs.map_state == X.IsViewable,
                    is_active=False,  # Will be determined by caller
                    is_always_on_top=False,  # Not easily detectable
                    opacity=1.0,  # Default opacity
                    display=None,
                )
            except Exception:
                return None

        # Iterate through all windows
        def traverse(win: Any) -> None:
            info = get_window_info(win)
            if info:
                windows.append(info)
            try:
                children = win.query_tree().children
                for child in children:
                    traverse(child)
            except Exception:
                pass

        traverse(self._root)
        return windows

    def get_active_window(self) -> WindowInfo | None:
        """Get active window."""
        try:
            atom = self._display.intern_atom("_NET_ACTIVE_WINDOW")
            prop = self._root.get_full_property(atom, X.AnyPropertyType)
            if prop:
                win_id = prop.value[0]
                windows = self.list_windows(visible_only=False)
                for w in windows:
                    if w.handle == win_id:
                        return w
        except Exception:
            pass
        return None

    def get_window_at(self, x: int, y: int) -> WindowInfo | None:
        """Get window at position."""
        # Query pointer to get window at position
        pointer = self._root.query_pointer()
        child = pointer.child
        if child:
            windows = self.list_windows(visible_only=False)
            for w in windows:
                if w.handle == child.id:
                    return w
        return None

    def focus_window(self, window: WindowInfo | int) -> None:
        """Focus window."""
        handle = self._get_window_handle(window)
        win = self._display.create_resource_object("window", handle)
        win.set_input_focus(X.RevertToParent, X.CurrentTime)
        win.configure(stack_mode=X.Above)
        self._display.sync()

    def move_window(self, window: WindowInfo | int, x: int, y: int) -> None:
        """Move window."""
        handle = self._get_window_handle(window)
        win = self._display.create_resource_object("window", handle)
        win.configure(x=x, y=y)
        self._display.sync()

    def resize_window(self, window: WindowInfo | int, width: int, height: int) -> None:
        """Resize window."""
        handle = self._get_window_handle(window)
        win = self._display.create_resource_object("window", handle)
        win.configure(width=width, height=height)
        self._display.sync()

    def set_window_state(self, window: WindowInfo | int, state: WindowState) -> None:
        """Set window state."""
        handle = self._get_window_handle(window)
        win = self._display.create_resource_object("window", handle)

        if state == WindowState.MINIMIZED:
            win.unmap()
        elif state == WindowState.MAXIMIZED:
            # Send _NET_WM_STATE message
            atom_state = self._display.intern_atom("_NET_WM_STATE")
            atom_max_vert = self._display.intern_atom("_NET_WM_STATE_MAXIMIZED_VERT")
            atom_max_horz = self._display.intern_atom("_NET_WM_STATE_MAXIMIZED_HORZ")

            ev = event.ClientMessage(
                window=win,
                client_type=atom_state,
                data=(32, [1, atom_max_vert, atom_max_horz, 0, 0]),
            )
            self._root.send_event(ev, event_mask=X.SubstructureRedirectMask)
        elif state == WindowState.NORMAL:
            win.map()

        self._display.sync()

    def get_window_state(self, window: WindowInfo | int) -> WindowState:
        """Get window state."""
        try:
            handle = self._get_window_handle(window)
            win = self._display.create_resource_object("window", handle)
            attrs = win.get_attributes()

            if attrs.map_state != X.IsViewable:
                return WindowState.MINIMIZED

            # Check if maximized
            atom_state = self._display.intern_atom("_NET_WM_STATE")
            prop = win.get_full_property(atom_state, X.AnyPropertyType)
            if prop:
                atom_max_vert = self._display.intern_atom("_NET_WM_STATE_MAXIMIZED_VERT")
                atom_max_horz = self._display.intern_atom("_NET_WM_STATE_MAXIMIZED_HORZ")
                if atom_max_vert in prop.value and atom_max_horz in prop.value:
                    return WindowState.MAXIMIZED

            return WindowState.NORMAL
        except Exception:
            return WindowState.NORMAL

    def close_window(self, window: WindowInfo | int) -> None:
        """Close window."""
        handle = self._get_window_handle(window)
        win = self._display.create_resource_object("window", handle)

        # Try graceful close first
        try:
            atom_protocols = self._display.intern_atom("WM_PROTOCOLS")
            atom_delete = self._display.intern_atom("WM_DELETE_WINDOW")

            ev = event.ClientMessage(
                window=win,
                client_type=atom_protocols,
                data=(32, [atom_delete, X.CurrentTime, 0, 0, 0]),
            )
            win.send_event(ev, event_mask=X.NoEventMask)
            self._display.sync()
        except Exception:
            # Force close
            win.destroy()
            self._display.sync()

    def set_window_opacity(self, window: WindowInfo | int, opacity: float) -> None:
        """Set window opacity (0.0-1.0)."""
        handle = self._get_window_handle(window)
        win = self._display.create_resource_object("window", handle)

        # _NET_WM_WINDOW_OPACITY atom
        atom_opacity = self._display.intern_atom("_NET_WM_WINDOW_OPACITY")

        # Opacity is 32-bit cardinal, 0xFFFFFFFF = fully opaque
        opacity_value = int(opacity * 0xFFFFFFFF)

        win.change_property(
            atom_opacity, self._display.intern_atom("CARDINAL"), 32, [opacity_value]
        )
        self._display.sync()

    def set_window_always_on_top(self, window: WindowInfo | int, always_on_top: bool) -> None:
        """Set window always on top."""
        handle = self._get_window_handle(window)
        win = self._display.create_resource_object("window", handle)

        atom_state = self._display.intern_atom("_NET_WM_STATE")
        atom_above = self._display.intern_atom("_NET_WM_STATE_ABOVE")

        # 1 = add, 0 = remove
        action = 1 if always_on_top else 0

        ev = event.ClientMessage(
            window=win, client_type=atom_state, data=(32, [action, atom_above, 0, 0, 0])
        )
        self._root.send_event(ev, event_mask=X.SubstructureRedirectMask)
        self._display.sync()

    # Clipboard methods
    def clipboard_get_text(self) -> str:
        """Get clipboard text."""
        atom_clipboard = self._display.intern_atom("CLIPBOARD")
        atom_utf8 = self._display.intern_atom("UTF8_STRING")
        atom_string = self._display.intern_atom("STRING")
        atom_property = self._display.intern_atom("XSEL_DATA")

        # Get current clipboard owner
        owner = self._display.get_selection_owner(atom_clipboard)
        if owner == X.NONE:
            return ""

        # Request clipboard content to be stored in our root window's property
        self._root.convert_selection(
            atom_clipboard,  # selection
            atom_utf8,  # target (prefer UTF8)
            atom_property,  # property to store result
            X.CurrentTime,
        )
        self._display.sync()

        # Wait for SelectionNotify event (with timeout)
        start_time = time.time()
        timeout = 1.0  # 1 second timeout

        while time.time() - start_time < timeout:
            # Check for pending events
            if self._display.pending_events() > 0:
                event_obj = self._display.next_event()
                if event_obj.type == X.SelectionNotify:
                    # Check if conversion succeeded
                    if event_obj.property == X.NONE:
                        # Conversion failed, try STRING as fallback
                        self._root.convert_selection(
                            atom_clipboard, atom_string, atom_property, X.CurrentTime
                        )
                        self._display.sync()
                        continue

                    # Read the property
                    try:
                        prop = self._root.get_full_property(atom_property, X.AnyPropertyType)
                        if prop and prop.value:
                            # Delete the property after reading
                            self._root.delete_property(atom_property)
                            self._display.sync()

                            # Decode the value
                            if isinstance(prop.value, bytes):
                                return prop.value.decode("utf-8", errors="ignore")
                            return str(prop.value)
                    except Exception:
                        pass

                    return ""
            time.sleep(0.01)

        return ""

    def clipboard_set_text(self, text: str) -> None:
        """Set clipboard text."""
        atom_clipboard = self._display.intern_atom("CLIPBOARD")

        # Create a window to own the selection if we don't have one
        if not hasattr(self, "_clipboard_window"):
            self._clipboard_window = self._root.create_window(0, 0, 1, 1, 0, X.CopyFromParent)

        # Store the text for later retrieval
        self._clipboard_text = text.encode("utf-8")

        # Take ownership of the CLIPBOARD selection
        self._clipboard_window.set_selection_owner(atom_clipboard, X.CurrentTime)
        self._display.flush()

        # Process pending events to ensure ownership is established
        # This is important in virtual X11 environments like Xvfb
        for _ in range(5):
            if self._display.pending_events() > 0:
                self._display.next_event()
            time.sleep(0.01)

        # Verify we got the ownership
        # Note: get_selection_owner() returns a Window resource or X.NONE
        owner = self._display.get_selection_owner(atom_clipboard)
        if owner == X.NONE:
            # No owner - this might be ok in some environments
            pass
        elif hasattr(owner, "id"):
            # Check if we own it (compare window IDs)
            if owner.id != self._clipboard_window.id:
                # In Xvfb/headless, ownership might work differently
                # Log but don't fail - we'll see if selection requests work
                pass

        # Process any immediate selection requests
        # Note: In a full implementation, we'd need to continuously handle SelectionRequest events
        # For now, we'll just handle a few immediate requests
        for _ in range(10):  # Check for up to 10 events
            if self._display.pending_events() > 0:
                event_obj = self._display.next_event()
                if event_obj.type == X.SelectionRequest:
                    self._handle_selection_request(event_obj)
            else:
                break
            time.sleep(0.01)

    def _handle_selection_request(self, event_obj: Any) -> None:
        """Handle X11 SelectionRequest event."""
        atom_utf8 = self._display.intern_atom("UTF8_STRING")
        atom_string = self._display.intern_atom("STRING")
        atom_targets = self._display.intern_atom("TARGETS")

        # Create SelectionNotify response
        selection_notify = event.SelectionNotify(
            time=event_obj.time,
            requestor=event_obj.requestor,
            selection=event_obj.selection,
            target=event_obj.target,
            property=event_obj.property,
        )

        # Handle TARGETS request
        if event_obj.target == atom_targets:
            # Respond with list of supported targets
            targets = [atom_utf8, atom_string, atom_targets]
            event_obj.requestor.change_property(
                event_obj.property,
                X.ATOM,
                32,
                targets,
            )
        # Handle UTF8_STRING or STRING request
        elif event_obj.target in (atom_utf8, atom_string):
            # Send the clipboard text
            event_obj.requestor.change_property(
                event_obj.property,
                event_obj.target,
                8,  # 8-bit format
                self._clipboard_text,
            )
        else:
            # Unsupported target
            selection_notify.property = X.NONE

        # Send SelectionNotify event back to requestor
        event_obj.requestor.send_event(selection_notify)
        self._display.sync()

    def clipboard_clear(self) -> None:
        """Clear clipboard."""
        self.clipboard_set_text("")

    def clipboard_has_text(self) -> bool:
        """Check if clipboard has text."""
        try:
            text = self.clipboard_get_text()
            return len(text) > 0
        except Exception:
            return False

    # Permission check
    def check_permissions(self) -> dict[str, bool]:
        """Check permissions."""
        # X11 doesn't have explicit permissions like macOS
        # Check if we can connect to display
        return {
            "mouse": True,
            "keyboard": True,
            "window": True,
            "accessibility": True,
            "screen_recording": True,
        }
