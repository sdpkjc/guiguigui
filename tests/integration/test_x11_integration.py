"""Integration tests for X11 backend.

These tests require actual X11 environment with virtual display (Xvfb).
They test real GUI operations to ensure the backend works correctly.
"""

from __future__ import annotations

import sys
import time

import pytest

from guiguigui.core.types import Key, MouseButton, Point

# Only run these tests on Linux with integration marker
pytestmark = [
    pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Linux/X11 only tests"),
    pytest.mark.integration,
]


class TestX11MouseIntegration:
    """Integration tests for mouse operations on X11."""

    def test_mouse_move_and_position(self) -> None:
        """Test moving mouse and getting position."""
        from guiguigui import mouse

        # Get current position
        start_pos = mouse.position()
        assert isinstance(start_pos, Point)

        # Move mouse
        target_x = start_pos.x + 100
        target_y = start_pos.y + 100
        mouse.move(target_x, target_y)

        # Check new position (allow small margin)
        time.sleep(0.1)
        new_pos = mouse.position()
        assert abs(new_pos.x - target_x) < 5
        assert abs(new_pos.y - target_y) < 5

        # Move back
        mouse.move(start_pos.x, start_pos.y)

    def test_mouse_relative_move(self) -> None:
        """Test relative mouse movement."""
        from guiguigui import mouse

        start_pos = mouse.position()

        # Move relatively
        mouse.move_rel(50, 50)
        time.sleep(0.05)

        new_pos = mouse.position()
        assert abs(new_pos.x - (start_pos.x + 50)) < 5
        assert abs(new_pos.y - (start_pos.y + 50)) < 5

        # Move back
        mouse.move(start_pos.x, start_pos.y)

    def test_mouse_click(self) -> None:
        """Test mouse click operation."""
        from guiguigui import mouse

        # Should not raise exception
        mouse.click()
        time.sleep(0.05)

    def test_mouse_double_click(self) -> None:
        """Test double click."""
        from guiguigui import mouse

        mouse.double_click()
        time.sleep(0.05)

    def test_mouse_right_click(self) -> None:
        """Test right click."""
        from guiguigui import mouse

        mouse.right_click()
        time.sleep(0.05)

    def test_mouse_scroll(self) -> None:
        """Test mouse scroll."""
        from guiguigui import mouse

        # Scroll up and down
        mouse.scroll(dy=3)
        time.sleep(0.05)
        mouse.scroll(dy=-3)
        time.sleep(0.05)

    def test_mouse_drag(self) -> None:
        """Test mouse drag operation."""
        from guiguigui import mouse

        start_pos = mouse.position()

        # Perform drag
        mouse.drag(start_pos.x + 50, start_pos.y + 50, duration=0.1)
        time.sleep(0.1)

        # Move back
        mouse.move(start_pos.x, start_pos.y)

    def test_mouse_context_manager(self) -> None:
        """Test mouse pressed context manager."""
        from guiguigui import mouse

        start_pos = mouse.position()

        with mouse.pressed(MouseButton.LEFT):
            mouse.move(start_pos.x + 30, start_pos.y + 30, duration=0.1)
            time.sleep(0.05)

        # Move back
        mouse.move(start_pos.x, start_pos.y)


class TestX11KeyboardIntegration:
    """Integration tests for keyboard operations on X11."""

    def test_keyboard_type(self) -> None:
        """Test typing text."""
        from guiguigui import keyboard

        # Type some text
        keyboard.type("test")
        time.sleep(0.1)

    @pytest.mark.skip(reason="Unicode typing not yet implemented for X11")
    def test_keyboard_unicode(self) -> None:
        """Test typing Unicode text."""
        from guiguigui import keyboard

        keyboard.type("中文😌")
        time.sleep(0.1)

    def test_keyboard_press_release(self) -> None:
        """Test press and release."""
        from guiguigui import keyboard

        keyboard.press(Key.SHIFT)
        time.sleep(0.05)
        keyboard.release(Key.SHIFT)
        time.sleep(0.05)

    def test_keyboard_tap(self) -> None:
        """Test tap key."""
        from guiguigui import keyboard

        keyboard.tap(Key.SPACE)
        time.sleep(0.05)

    def test_keyboard_hotkey(self) -> None:
        """Test hotkey combination."""
        from guiguigui import keyboard

        # Ctrl+A (Select All)
        keyboard.hotkey(Key.CTRL, Key.A)
        time.sleep(0.1)

    def test_keyboard_context_manager(self) -> None:
        """Test keyboard pressed context manager."""
        from guiguigui import keyboard

        with keyboard.pressed(Key.SHIFT):
            keyboard.tap(Key.A)
            time.sleep(0.05)

    def test_keyboard_layout(self) -> None:
        """Test getting keyboard layout."""
        from guiguigui import keyboard

        layout = keyboard.layout()
        assert isinstance(layout, str)
        assert len(layout) > 0


class TestX11DisplayIntegration:
    """Integration tests for display operations on X11."""

    def test_display_list(self) -> None:
        """Test listing all displays."""
        from guiguigui import display

        displays = display.list()
        assert len(displays) >= 1

        for d in displays:
            assert d.bounds.width > 0
            assert d.bounds.height > 0
            assert d.scale > 0

    def test_display_primary(self) -> None:
        """Test getting primary display."""
        from guiguigui import display

        primary = display.primary()
        assert primary.is_primary is True
        assert primary.bounds.width > 0
        assert primary.bounds.height > 0

    def test_display_at_point(self) -> None:
        """Test getting display at point."""
        from guiguigui import display

        primary = display.primary()
        center_x = primary.bounds.width // 2
        center_y = primary.bounds.height // 2

        disp = display.at(center_x, center_y)
        assert disp is not None

    def test_display_virtual_screen(self) -> None:
        """Test virtual screen rect."""
        from guiguigui import display

        rect = display.virtual_screen_rect()
        assert rect.width > 0
        assert rect.height > 0


class TestX11WindowIntegration:
    """Integration tests for window operations on X11."""

    def test_window_list(self) -> None:
        """Test listing windows."""
        from guiguigui import window

        windows = window.list()
        assert isinstance(windows, list)

    def test_window_active(self) -> None:
        """Test getting active window."""
        from guiguigui import window

        active = window.active()
        # Might be None, but should not raise
        if active:
            assert hasattr(active, "title")

    def test_window_find(self) -> None:
        """Test finding window by title."""
        from guiguigui import window

        # Try to find any window
        result = window.find(title="")
        # Result might be None or a window
        assert result is None or hasattr(result, "title")

    def test_window_at_mouse(self) -> None:
        """Test getting window at mouse position."""
        from guiguigui import mouse, window

        pos = mouse.position()
        win = window.at(pos.x, pos.y)

        # Might be None if mouse is not over a window
        if win:
            assert hasattr(win, "title")


class TestX11ClipboardIntegration:
    """Integration tests for clipboard operations on X11."""

    @pytest.mark.skip(reason="X11 clipboard operations not yet fully implemented")
    def test_clipboard_set_get(self) -> None:
        """Test setting and getting clipboard."""
        from guiguigui import clipboard

        # Save original
        original = clipboard.get()

        # Test set and get
        test_text = "GuiGuiGui Integration Test"
        clipboard.set(test_text)
        time.sleep(0.05)

        result = clipboard.get()
        assert result == test_text

        # Restore
        clipboard.set(original)


class TestX11Permissions:
    """Test permission-related functionality."""

    def test_check_permissions(self) -> None:
        """Test checking permissions."""
        from guiguigui.backend import get_backend

        backend = get_backend()
        perms = backend.check_permissions()

        assert isinstance(perms, dict)
        assert "accessibility" in perms
        assert "mouse" in perms
        assert "keyboard" in perms

        # Print permission status for debugging
        print("\nPermission status:")
        for key, value in perms.items():
            print(f"  {key}: {value}")


class TestX11EndToEnd:
    """End-to-end integration tests."""

    def test_complete_workflow(self) -> None:
        """Test a complete workflow using multiple components."""
        from guiguigui import display, keyboard, mouse

        # 1. Get display info
        primary = display.primary()
        assert primary.bounds.width > 0

        # 2. Move mouse to center
        center_x = primary.bounds.width // 2
        center_y = primary.bounds.height // 2
        mouse.move(center_x, center_y, duration=0.2)
        time.sleep(0.1)

        # 3. Type some text
        keyboard.type("Hello")
        time.sleep(0.1)

    def test_macro_like_operations(self) -> None:
        """Test macro-like sequence of operations."""
        from guiguigui import keyboard, mouse

        start_pos = mouse.position()

        # Move and click
        mouse.move(start_pos.x + 50, start_pos.y + 50, duration=0.1)
        time.sleep(0.05)
        mouse.click()
        time.sleep(0.05)

        # Type with modifiers
        with keyboard.pressed(Key.SHIFT):
            keyboard.tap(Key.A)
        time.sleep(0.05)

        # Move back
        mouse.move(start_pos.x, start_pos.y)
