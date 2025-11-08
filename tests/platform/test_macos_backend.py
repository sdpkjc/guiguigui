"""Unit tests for macOS backend implementation.

These tests verify the macOS-specific backend logic and methods.
"""

from __future__ import annotations

import sys

import pytest

# Only run these tests on macOS
pytestmark = pytest.mark.skipif(sys.platform != "darwin", reason="macOS only tests")


class TestMacOSBackendImport:
    """Test macOS backend can be imported and instantiated."""

    def test_import_macos_backend(self) -> None:
        """Test that macOS backend can be imported."""
        from guiguigui.backend.macos import MacOSBackend

        assert MacOSBackend is not None

    def test_create_macos_backend(self) -> None:
        """Test that macOS backend can be instantiated."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        assert backend is not None

    def test_backend_has_required_methods(self) -> None:
        """Test that backend implements all required abstract methods."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Mouse methods
        assert hasattr(backend, "mouse_position")
        assert hasattr(backend, "mouse_move_to")
        assert hasattr(backend, "mouse_move_rel")
        assert hasattr(backend, "mouse_press")
        assert hasattr(backend, "mouse_release")
        assert hasattr(backend, "mouse_scroll")
        assert hasattr(backend, "mouse_is_pressed")

        # Keyboard methods
        assert hasattr(backend, "key_press")
        assert hasattr(backend, "key_release")
        assert hasattr(backend, "key_is_pressed")
        assert hasattr(backend, "key_type_unicode")
        assert hasattr(backend, "get_keyboard_layout")

        # Display methods
        assert hasattr(backend, "get_displays")
        assert hasattr(backend, "get_primary_display")
        assert hasattr(backend, "get_virtual_screen_rect")

        # Window methods
        assert hasattr(backend, "list_windows")
        assert hasattr(backend, "get_active_window")
        assert hasattr(backend, "get_window_at")
        assert hasattr(backend, "focus_window")
        assert hasattr(backend, "move_window")
        assert hasattr(backend, "resize_window")
        assert hasattr(backend, "set_window_state")
        assert hasattr(backend, "get_window_state")
        assert hasattr(backend, "close_window")
        assert hasattr(backend, "set_window_opacity")
        assert hasattr(backend, "set_window_always_on_top")

        # Clipboard methods
        assert hasattr(backend, "clipboard_get_text")
        assert hasattr(backend, "clipboard_set_text")
        assert hasattr(backend, "clipboard_clear")
        assert hasattr(backend, "clipboard_has_text")

        # Permission check
        assert hasattr(backend, "check_permissions")


class TestMacOSKeyMapping:
    """Test key code mapping for macOS."""

    def test_key_mapping_exists(self) -> None:
        """Test that key mapping dictionary exists."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        # Check that _key_code_map is defined
        assert hasattr(backend, "_key_code_map")
        assert isinstance(backend._key_code_map, dict)

    def test_common_keys_mapped(self) -> None:
        """Test that common keys have mappings."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Test some common keys exist in mapping
        common_keys = [
            "a",
            "return",
            "space",
            "shift",
            "command",
            "escape",
            "delete",
        ]

        for key in common_keys:
            assert key in backend._key_code_map, f"Key {key} should be in key code map"


class TestMacOSMouseButton:
    """Test mouse button operations for macOS."""

    def test_mouse_button_press_release(self) -> None:
        """Test mouse button press and release operations."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import MouseButton

        backend = MacOSBackend()

        # These should not raise exceptions
        # Just test that the methods work
        backend.mouse_press(MouseButton.LEFT)
        backend.mouse_release(MouseButton.LEFT)

    def test_mouse_is_pressed_returns_bool(self) -> None:
        """Test that mouse_is_pressed returns a boolean."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import MouseButton

        backend = MacOSBackend()

        # Should return a boolean for all button types
        result_left = backend.mouse_is_pressed(MouseButton.LEFT)
        result_right = backend.mouse_is_pressed(MouseButton.RIGHT)
        result_middle = backend.mouse_is_pressed(MouseButton.MIDDLE)

        assert isinstance(result_left, bool)
        assert isinstance(result_right, bool)
        assert isinstance(result_middle, bool)


class TestMacOSMouseMovement:
    """Test mouse movement operations for macOS."""

    def test_mouse_move_to_executes(self) -> None:
        """Test that mouse_move_to moves cursor to target position."""
        import time

        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Get current position as reference
        start_pos = backend.mouse_position()

        # Move to specific positions and verify
        # Note: macOS backend doesn't support duration parameter
        backend.mouse_move_to(100, 100)
        time.sleep(0.05)  # Small delay for system to process
        pos1 = backend.mouse_position()
        assert pos1.x == 100, f"Expected x=100, got {pos1.x}"
        assert pos1.y == 100, f"Expected y=100, got {pos1.y}"

        backend.mouse_move_to(200, 200)
        time.sleep(0.05)
        pos2 = backend.mouse_position()
        assert pos2.x == 200, f"Expected x=200, got {pos2.x}"
        assert pos2.y == 200, f"Expected y=200, got {pos2.y}"

        # Move back to original position
        backend.mouse_move_to(start_pos.x, start_pos.y)

    def test_mouse_move_to_instant(self) -> None:
        """Test instant mouse movement (macOS always instant)."""
        import time

        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        start_pos = backend.mouse_position()

        # macOS backend always performs instant moves (no duration parameter)
        target_x = start_pos.x + 50
        target_y = start_pos.y + 50
        backend.mouse_move_to(target_x, target_y)

        # Verify position changed to target
        time.sleep(0.05)
        new_pos = backend.mouse_position()
        assert new_pos.x == target_x, f"Expected x={target_x}, got {new_pos.x}"
        assert new_pos.y == target_y, f"Expected y={target_y}, got {new_pos.y}"

        # Restore original position
        backend.mouse_move_to(start_pos.x, start_pos.y)

    def test_mouse_move_rel_executes(self) -> None:
        """Test that mouse_move_rel moves cursor relatively."""
        import time

        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Get starting position
        start_pos = backend.mouse_position()

        # Move relatively and verify position change
        backend.mouse_move_rel(30, 40)
        time.sleep(0.05)
        pos1 = backend.mouse_position()
        assert pos1.x == start_pos.x + 30, f"Expected x={start_pos.x + 30}, got {pos1.x}"
        assert pos1.y == start_pos.y + 40, f"Expected y={start_pos.y + 40}, got {pos1.y}"

        # Move back relatively
        backend.mouse_move_rel(-30, -40)
        time.sleep(0.05)
        pos2 = backend.mouse_position()
        assert pos2.x == start_pos.x, f"Expected x={start_pos.x}, got {pos2.x}"
        assert pos2.y == start_pos.y, f"Expected y={start_pos.y}, got {pos2.y}"

    def test_mouse_move_to_negative_coordinates(self) -> None:
        """Test mouse_move_to with negative coordinates."""
        import time

        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Store original position
        original = backend.mouse_position()

        # Negative coordinates should not crash
        # macOS allows negative coordinates (for multi-monitor setups)
        backend.mouse_move_to(-100, -100)
        time.sleep(0.05)

        # Verify position was set (macOS accepts negative coordinates)
        pos = backend.mouse_position()
        assert isinstance(pos.x, int), "Position x should be an integer"
        assert isinstance(pos.y, int), "Position y should be an integer"
        assert pos.x == -100, f"Expected x=-100, got {pos.x}"
        assert pos.y == -100, f"Expected y=-100, got {pos.y}"

        # Restore original position
        backend.mouse_move_to(original.x, original.y)

    def test_mouse_move_to_large_coordinates(self) -> None:
        """Test mouse_move_to with very large coordinates."""
        import time

        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Store original position
        original = backend.mouse_position()

        # Large coordinates should not crash
        # macOS allows large coordinates (for multi-monitor setups)
        backend.mouse_move_to(10000, 10000)
        time.sleep(0.05)

        # Verify position was set (macOS accepts large coordinates)
        pos = backend.mouse_position()
        assert isinstance(pos.x, int), "Position x should be an integer"
        assert isinstance(pos.y, int), "Position y should be an integer"
        assert pos.x == 10000, f"Expected x=10000, got {pos.x}"
        assert pos.y == 10000, f"Expected y=10000, got {pos.y}"

        # Restore original position
        backend.mouse_move_to(original.x, original.y)


class TestMacOSMouseScroll:
    """Test mouse scroll operations for macOS."""

    def test_mouse_scroll_vertical(self) -> None:
        """Test vertical mouse scroll."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Vertical scroll should not raise
        backend.mouse_scroll(0, 5)  # Scroll up
        backend.mouse_scroll(0, -5)  # Scroll down

    def test_mouse_scroll_horizontal(self) -> None:
        """Test horizontal mouse scroll."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Horizontal scroll should not raise
        backend.mouse_scroll(5, 0)  # Scroll right
        backend.mouse_scroll(-5, 0)  # Scroll left

    def test_mouse_scroll_diagonal(self) -> None:
        """Test diagonal mouse scroll."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Diagonal scroll should not raise
        backend.mouse_scroll(3, 3)

    def test_mouse_scroll_zero(self) -> None:
        """Test mouse scroll with zero values."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Zero scroll should not raise
        backend.mouse_scroll(0, 0)

    def test_mouse_scroll_large_values(self) -> None:
        """Test mouse scroll with large values."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Large scroll values should not crash
        backend.mouse_scroll(100, 100)


class TestMacOSPermissions:
    """Test permission checking on macOS."""

    def test_check_permissions_returns_dict(self) -> None:
        """Test that check_permissions returns a dictionary."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        try:
            perms = backend.check_permissions()

            assert isinstance(perms, dict)
            assert "accessibility" in perms
            assert "screen_recording" in perms
            assert isinstance(perms["accessibility"], bool)
            assert isinstance(perms["screen_recording"], bool)
        except AttributeError:
            # AXIsProcessTrusted might not be available in some environments
            pytest.skip("Permission check API not available")


class TestMacOSKeyboard:
    """Test keyboard operations for macOS."""

    def test_key_is_pressed_returns_bool(self) -> None:
        """Test that key_is_pressed returns a boolean."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import Key

        backend = MacOSBackend()

        # Should return a boolean for various key types
        result_shift = backend.key_is_pressed(Key.SHIFT)
        result_a = backend.key_is_pressed("a")
        result_space = backend.key_is_pressed(Key.SPACE)

        assert isinstance(result_shift, bool)
        assert isinstance(result_a, bool)
        assert isinstance(result_space, bool)


class TestMacOSKeyboardPressRelease:
    """Test keyboard press and release operations for macOS."""

    def test_key_press_release_with_key_enum(self) -> None:
        """Test key press and release with Key enum."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import Key

        backend = MacOSBackend()

        # Press and release should not raise
        backend.key_press(Key.SHIFT)
        backend.key_release(Key.SHIFT)

        backend.key_press(Key.CTRL)
        backend.key_release(Key.CTRL)

    def test_key_press_release_with_string(self) -> None:
        """Test key press and release with string."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Press and release should not raise
        backend.key_press("a")
        backend.key_release("a")

        backend.key_press("1")
        backend.key_release("1")

    def test_key_press_release_special_keys(self) -> None:
        """Test special keys press and release."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import Key

        backend = MacOSBackend()

        # Test various special keys
        special_keys = [
            Key.ENTER,
            Key.TAB,
            Key.ESCAPE,
            Key.SPACE,
            Key.BACKSPACE,
            Key.DELETE,
        ]

        for key in special_keys:
            backend.key_press(key)
            backend.key_release(key)

    def test_key_press_release_function_keys(self) -> None:
        """Test function keys press and release."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import Key

        backend = MacOSBackend()

        # Test F1-F4
        backend.key_press(Key.F1)
        backend.key_release(Key.F1)

        backend.key_press(Key.F12)
        backend.key_release(Key.F12)

    def test_key_press_release_arrow_keys(self) -> None:
        """Test arrow keys press and release."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import Key

        backend = MacOSBackend()

        # Test all arrow keys
        backend.key_press(Key.UP)
        backend.key_release(Key.UP)

        backend.key_press(Key.DOWN)
        backend.key_release(Key.DOWN)

        backend.key_press(Key.LEFT)
        backend.key_release(Key.LEFT)

        backend.key_press(Key.RIGHT)
        backend.key_release(Key.RIGHT)


class TestMacOSKeyboardTyping:
    """Test keyboard typing operations for macOS."""

    def test_key_type_unicode_ascii(self) -> None:
        """Test typing ASCII characters."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Should not raise for ASCII
        backend.key_type_unicode("a")
        backend.key_type_unicode("A")
        backend.key_type_unicode("1")
        backend.key_type_unicode("!")

    def test_key_type_unicode_string(self) -> None:
        """Test typing multi-character string."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Should not raise for strings
        backend.key_type_unicode("hello")
        backend.key_type_unicode("Hello World")

    def test_key_type_unicode_unicode(self) -> None:
        """Test typing Unicode characters."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Should not raise for Unicode
        backend.key_type_unicode("你好")
        backend.key_type_unicode("🌍")
        backend.key_type_unicode("こんにちは")

    def test_key_type_unicode_special_chars(self) -> None:
        """Test typing special characters."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Should not raise for special chars
        backend.key_type_unicode("@#$%")
        backend.key_type_unicode("\n\t")

    def test_key_type_unicode_empty_string(self) -> None:
        """Test typing empty string."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Empty string should not raise
        backend.key_type_unicode("")


class TestMacOSKeyboardLayout:
    """Test keyboard layout detection."""

    def test_get_keyboard_layout_returns_string(self) -> None:
        """Test that get_keyboard_layout returns a string."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        layout = backend.get_keyboard_layout()

        assert isinstance(layout, str)
        assert len(layout) > 0

    def test_keyboard_layout_format(self) -> None:
        """Test that keyboard layout has expected format."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        layout = backend.get_keyboard_layout()

        # Should be something like "com.apple.keylayout.US"
        assert "." in layout or layout != ""


class TestMacOSDisplay:
    """Test display-related methods."""

    def test_get_displays_returns_list(self) -> None:
        """Test that get_displays returns a list."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        displays = backend.get_displays()

        assert isinstance(displays, list)
        assert len(displays) > 0

    def test_display_info_structure(self) -> None:
        """Test that DisplayInfo has correct structure."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        displays = backend.get_displays()

        for display in displays:
            assert hasattr(display, "id")
            assert hasattr(display, "name")
            assert hasattr(display, "bounds")
            assert hasattr(display, "scale")
            assert hasattr(display, "is_primary")
            assert display.bounds.width > 0
            assert display.bounds.height > 0
            assert display.scale > 0

    def test_get_primary_display(self) -> None:
        """Test that primary display can be retrieved."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        primary = backend.get_primary_display()

        assert primary is not None
        assert primary.is_primary is True

    def test_virtual_screen_rect(self) -> None:
        """Test virtual screen rect calculation."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        rect = backend.get_virtual_screen_rect()

        assert rect.width > 0
        assert rect.height > 0


class TestMacOSClipboard:
    """Test clipboard operations."""

    def test_clipboard_set_and_get(self) -> None:
        """Test setting and getting clipboard text."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Save original
        original = backend.clipboard_get_text()

        # Test set and get
        test_text = "GuiGuiGui Test"
        backend.clipboard_set_text(test_text)
        result = backend.clipboard_get_text()

        assert result == test_text

        # Restore original
        backend.clipboard_set_text(original)

    def test_clipboard_has_text(self) -> None:
        """Test checking if clipboard has text."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        backend.clipboard_set_text("test")
        assert backend.clipboard_has_text() is True

        backend.clipboard_clear()
        # After clear, might still have text or not depending on system
        # Just check it returns a boolean
        assert isinstance(backend.clipboard_has_text(), bool)

    def test_clipboard_clear(self) -> None:
        """Test clearing clipboard."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        backend.clipboard_set_text("test")
        backend.clipboard_clear()

        # Clear should work without error
        assert True


class TestMacOSWindow:
    """Test window-related methods."""

    def test_list_windows_returns_list(self) -> None:
        """Test that list_windows returns a list."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        windows = backend.list_windows()

        assert isinstance(windows, list)

    def test_get_active_window(self) -> None:
        """Test getting active window."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        active = backend.get_active_window()

        # Might be None if no windows, but should not raise
        if active:
            assert hasattr(active, "title")
            assert hasattr(active, "handle")

    def test_window_manipulation_raises_capability_error(self) -> None:
        """Test that window manipulation methods raise BackendCapabilityError on macOS."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.errors import BackendCapabilityError
        from guiguigui.core.types import WindowState

        backend = MacOSBackend()

        # Get a window handle (or use a dummy value if no windows)
        windows = backend.list_windows()
        if not windows:
            pytest.skip("No windows available for testing")

        handle = windows[0].handle

        # These methods should raise BackendCapabilityError on macOS
        with pytest.raises(BackendCapabilityError):
            backend.move_window(handle, 100, 100)

        with pytest.raises(BackendCapabilityError):
            backend.resize_window(handle, 800, 600)

        with pytest.raises(BackendCapabilityError):
            backend.set_window_state(handle, WindowState.MAXIMIZED)

        with pytest.raises(BackendCapabilityError):
            backend.close_window(handle)

        with pytest.raises(BackendCapabilityError):
            backend.set_window_opacity(handle, 0.8)

        with pytest.raises(BackendCapabilityError):
            backend.set_window_always_on_top(handle, True)

    def test_window_get_state(self) -> None:
        """Test that get_window_state returns a WindowState."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import WindowState

        backend = MacOSBackend()
        windows = backend.list_windows()

        if not windows:
            pytest.skip("No windows available for testing")

        handle = windows[0].handle

        # get_window_state should not raise, but always returns NORMAL on macOS
        state = backend.get_window_state(handle)
        assert isinstance(state, WindowState)
        assert state == WindowState.NORMAL


class TestMacOSEventHooks:
    """Test event hook methods."""

    def test_hook_methods_raise_not_implemented(self) -> None:
        """Test that hook methods raise NotImplementedError."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Hook methods should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            backend.hook_mouse(lambda event: True)

        with pytest.raises(NotImplementedError):
            backend.hook_keyboard(lambda event: True)

        with pytest.raises(NotImplementedError):
            backend.unhook(None)


class TestMacOSCoordinateSystem:
    """Test coordinate system handling."""

    def test_mouse_position_in_bounds(self) -> None:
        """Test that mouse position is within screen bounds."""
        import time

        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        rect = backend.get_virtual_screen_rect()

        # Move to a known position within bounds first
        backend.mouse_move_to(100, 100)
        time.sleep(0.05)  # Small delay to ensure move completes
        pos = backend.mouse_position()

        # Position should be within virtual screen
        assert pos.x >= rect.x
        assert pos.y >= rect.y
        # Allow some margin for multi-monitor setups
        assert pos.x <= rect.x + rect.width + 1000
        assert pos.y <= rect.y + rect.height + 1000


class TestMacOSMouseButtonEdgeCases:
    """Test mouse button edge cases including unsupported buttons."""

    def test_mouse_press_unsupported_button_x1(self) -> None:
        """Test that pressing X1 button raises ValueError."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import MouseButton

        backend = MacOSBackend()

        # X1 button is not supported on macOS
        with pytest.raises(ValueError, match="Unsupported button"):
            backend.mouse_press(MouseButton.X1)

    def test_mouse_press_unsupported_button_x2(self) -> None:
        """Test that pressing X2 button raises ValueError."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import MouseButton

        backend = MacOSBackend()

        # X2 button is not supported on macOS
        with pytest.raises(ValueError, match="Unsupported button"):
            backend.mouse_press(MouseButton.X2)

    def test_mouse_release_unsupported_button_x1(self) -> None:
        """Test that releasing X1 button raises ValueError."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import MouseButton

        backend = MacOSBackend()

        # X1 button is not supported on macOS
        with pytest.raises(ValueError, match="Unsupported button"):
            backend.mouse_release(MouseButton.X1)

    def test_mouse_release_unsupported_button_x2(self) -> None:
        """Test that releasing X2 button raises ValueError."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import MouseButton

        backend = MacOSBackend()

        # X2 button is not supported on macOS
        with pytest.raises(ValueError, match="Unsupported button"):
            backend.mouse_release(MouseButton.X2)

    def test_mouse_is_pressed_unsupported_button_x1(self) -> None:
        """Test that checking X1 button state raises ValueError."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import MouseButton

        backend = MacOSBackend()

        # X1 button is not supported on macOS
        with pytest.raises(ValueError, match="Unsupported button"):
            backend.mouse_is_pressed(MouseButton.X1)

    def test_mouse_is_pressed_unsupported_button_x2(self) -> None:
        """Test that checking X2 button state raises ValueError."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import MouseButton

        backend = MacOSBackend()

        # X2 button is not supported on macOS
        with pytest.raises(ValueError, match="Unsupported button"):
            backend.mouse_is_pressed(MouseButton.X2)


class TestMacOSKeyboardUnicodeEdgeCases:
    """Test keyboard unicode typing edge cases."""

    def test_key_type_unicode_uppercase_with_shift(self) -> None:
        """Test that uppercase characters use shift key."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Uppercase characters should trigger shift key handling
        # This tests lines 236-249 in macos.py
        backend.key_type_unicode("A")
        backend.key_type_unicode("Z")
        backend.key_type_unicode("HELLO")

    def test_key_type_unicode_mixed_case(self) -> None:
        """Test typing mixed case string."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Mixed case should use shift for uppercase letters
        backend.key_type_unicode("HelloWorld")
        backend.key_type_unicode("TeSt123")

    def test_key_type_unicode_unmapped_characters(self) -> None:
        """Test typing characters not in key map uses unicode method."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # These characters are not in _key_code_map, so should use
        # CGEventKeyboardSetUnicodeString (lines 250-262)
        backend.key_type_unicode("©")  # Copyright symbol
        backend.key_type_unicode("™")  # Trademark symbol
        backend.key_type_unicode("€")  # Euro symbol
        backend.key_type_unicode("±")  # Plus-minus symbol

    def test_key_type_unicode_mixed_mapped_unmapped(self) -> None:
        """Test typing mix of mapped and unmapped characters."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Mix of regular characters and unicode symbols
        backend.key_type_unicode("a©b™c")
        backend.key_type_unicode("Price: €99")


class TestMacOSKeyboardInvalidKey:
    """Test keyboard with invalid key codes."""

    def test_key_press_invalid_key(self) -> None:
        """Test that pressing invalid key raises ValueError."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Invalid key should raise ValueError
        with pytest.raises(ValueError, match="Unknown key"):
            backend.key_press("invalid_key_xyz")

    def test_key_release_invalid_key(self) -> None:
        """Test that releasing invalid key raises ValueError."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Invalid key should raise ValueError
        with pytest.raises(ValueError, match="Unknown key"):
            backend.key_release("nonexistent_key")

    def test_get_key_code_with_key_enum(self) -> None:
        """Test _get_key_code with Key enum."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import Key

        backend = MacOSBackend()

        # Should work with Key enum
        key_code = backend._get_key_code(Key.SHIFT)
        assert isinstance(key_code, int)
        assert key_code == backend._key_code_map["shift"]


class TestMacOSKeyCodeMapping:
    """Test comprehensive key code mapping."""

    def test_all_letters_mapped(self) -> None:
        """Test that all letters a-z are mapped."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        for char in "abcdefghijklmnopqrstuvwxyz":
            assert char in backend._key_code_map, f"Letter {char} should be mapped"
            assert isinstance(backend._key_code_map[char], int)

    def test_all_digits_mapped(self) -> None:
        """Test that all digits 0-9 are mapped."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        for digit in "0123456789":
            assert digit in backend._key_code_map, f"Digit {digit} should be mapped"
            assert isinstance(backend._key_code_map[digit], int)

    def test_modifier_keys_mapped(self) -> None:
        """Test that modifier keys are mapped."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        modifiers = ["shift", "ctrl", "control", "alt", "option", "cmd", "command", "meta"]
        for mod in modifiers:
            assert mod in backend._key_code_map, f"Modifier {mod} should be mapped"

    def test_function_keys_mapped(self) -> None:
        """Test that function keys F1-F15 are mapped."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        for i in range(1, 16):
            key = f"f{i}"
            assert key in backend._key_code_map, f"Function key {key} should be mapped"

    def test_reverse_key_map(self) -> None:
        """Test that reverse key map is built correctly."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Check reverse map exists
        assert hasattr(backend, "_reverse_key_map")
        assert isinstance(backend._reverse_key_map, dict)

        # Verify reverse mapping exists for all codes
        # Note: Some keys like "enter"/"return" share the same code,
        # so the reverse map will only have one entry per code
        for _key, code in backend._key_code_map.items():
            assert code in backend._reverse_key_map
            # The reverse map should map back to one of the keys that shares this code
            reverse_key = backend._reverse_key_map[code]
            assert backend._key_code_map[reverse_key] == code


class TestMacOSWindowFiltering:
    """Test window filtering edge cases."""

    def test_list_windows_visible_only(self) -> None:
        """Test listing windows with visible_only flag."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Test with visible_only=True
        visible_windows = backend.list_windows(visible_only=True)
        assert isinstance(visible_windows, list)

        # Test with visible_only=False
        all_windows = backend.list_windows(visible_only=False)
        assert isinstance(all_windows, list)

        # All windows should include visible ones (might be more)
        assert len(all_windows) >= len(visible_windows)

    def test_window_info_completeness(self) -> None:
        """Test that WindowInfo has all expected fields."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        windows = backend.list_windows(visible_only=False)

        if not windows:
            pytest.skip("No windows available for testing")

        window = windows[0]

        # Check all fields are present
        assert hasattr(window, "handle")
        assert hasattr(window, "title")
        assert hasattr(window, "class_name")
        assert hasattr(window, "pid")
        assert hasattr(window, "process_name")
        assert hasattr(window, "rect")
        assert hasattr(window, "client_rect")
        assert hasattr(window, "state")
        assert hasattr(window, "is_visible")
        assert hasattr(window, "is_active")
        assert hasattr(window, "is_always_on_top")
        assert hasattr(window, "opacity")

        # Verify window has non-zero size (zero-size windows are filtered)
        assert window.rect.width > 0
        assert window.rect.height > 0


class TestMacOSWindowPositioning:
    """Test window positioning methods."""

    def test_get_window_at_valid_position(self) -> None:
        """Test getting window at a specific position."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        windows = backend.list_windows(visible_only=True)

        if not windows:
            pytest.skip("No windows available for testing")

        # Get first window's center position
        window = windows[0]
        center_x = window.rect.x + window.rect.width // 2
        center_y = window.rect.y + window.rect.height // 2

        # Should find a window at this position
        found_window = backend.get_window_at(center_x, center_y)

        # Might find the window or another window on top of it
        # Just verify it returns None or a WindowInfo
        assert found_window is None or hasattr(found_window, "handle")

    def test_get_window_at_empty_position(self) -> None:
        """Test getting window at empty screen position."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Try position far off screen where no window should be
        result = backend.get_window_at(-10000, -10000)

        # Should return None when no window at position
        assert result is None

    def test_get_window_at_origin(self) -> None:
        """Test getting window at screen origin."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Test at origin (0, 0)
        result = backend.get_window_at(0, 0)

        # Should return None or a valid window
        assert result is None or hasattr(result, "handle")


class TestMacOSDisplayEdgeCases:
    """Test display-related edge cases."""

    def test_display_scale_factor(self) -> None:
        """Test that display scale factor is valid."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        displays = backend.get_displays()

        assert len(displays) > 0

        for display in displays:
            # Scale should be positive and reasonable (1.0, 2.0 for Retina, etc.)
            assert display.scale > 0
            assert display.scale <= 3.0  # Common scales: 1.0, 1.5, 2.0, 2.5

    def test_display_refresh_rate(self) -> None:
        """Test that display refresh rate is valid or defaults to 60."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        displays = backend.get_displays()

        assert len(displays) > 0

        for display in displays:
            # Refresh rate should be positive (defaults to 60.0 if 0)
            assert display.refresh_rate > 0
            # Common refresh rates: 60, 120, 144
            assert 30 <= display.refresh_rate <= 240

    def test_display_physical_size(self) -> None:
        """Test that display physical size matches logical size times scale."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        displays = backend.get_displays()

        assert len(displays) > 0

        for display in displays:
            # Physical size should be logical size * scale
            expected_width = int(display.bounds.width * display.scale)
            expected_height = int(display.bounds.height * display.scale)

            assert display.physical_size.width == expected_width
            assert display.physical_size.height == expected_height

    def test_display_work_area_valid(self) -> None:
        """Test that display work area is valid."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        displays = backend.get_displays()

        assert len(displays) > 0

        for display in displays:
            # Work area should exist and have positive dimensions
            assert display.work_area.width > 0
            assert display.work_area.height > 0

            # Work area should be within or equal to bounds
            # (On macOS, work_area is same as bounds currently)
            assert display.work_area.width <= display.bounds.width
            assert display.work_area.height <= display.bounds.height

    def test_one_primary_display(self) -> None:
        """Test that exactly one display is marked as primary."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        displays = backend.get_displays()

        assert len(displays) > 0

        primary_count = sum(1 for d in displays if d.is_primary)
        assert primary_count == 1, "Exactly one display should be primary"

    def test_virtual_screen_encompasses_all_displays(self) -> None:
        """Test that virtual screen rect encompasses all displays."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        displays = backend.get_displays()
        virtual_rect = backend.get_virtual_screen_rect()

        assert len(displays) > 0

        for display in displays:
            # Each display should be within virtual screen bounds
            # Display left edge >= virtual left edge
            assert display.bounds.x >= virtual_rect.x
            # Display top edge >= virtual top edge
            assert display.bounds.y >= virtual_rect.y
            # Display right edge <= virtual right edge
            assert display.bounds.x + display.bounds.width <= virtual_rect.x + virtual_rect.width
            # Display bottom edge <= virtual bottom edge
            assert display.bounds.y + display.bounds.height <= virtual_rect.y + virtual_rect.height


class TestMacOSClipboardEdgeCases:
    """Test clipboard edge cases."""

    def test_clipboard_empty_string(self) -> None:
        """Test setting empty string to clipboard."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Save original
        original = backend.clipboard_get_text()

        # Set empty string
        backend.clipboard_set_text("")
        result = backend.clipboard_get_text()

        assert result == ""

        # Restore original
        backend.clipboard_set_text(original)

    def test_clipboard_unicode_text(self) -> None:
        """Test setting Unicode text to clipboard."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Save original
        original = backend.clipboard_get_text()

        # Set Unicode text
        test_text = "Hello 世界 🌍"
        backend.clipboard_set_text(test_text)
        result = backend.clipboard_get_text()

        assert result == test_text

        # Restore original
        backend.clipboard_set_text(original)

    def test_clipboard_multiline_text(self) -> None:
        """Test setting multiline text to clipboard."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Save original
        original = backend.clipboard_get_text()

        # Set multiline text
        test_text = "Line 1\nLine 2\nLine 3"
        backend.clipboard_set_text(test_text)
        result = backend.clipboard_get_text()

        assert result == test_text

        # Restore original
        backend.clipboard_set_text(original)

    def test_clipboard_long_text(self) -> None:
        """Test setting very long text to clipboard."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Save original
        original = backend.clipboard_get_text()

        # Set long text (10,000 characters)
        test_text = "A" * 10000
        backend.clipboard_set_text(test_text)
        result = backend.clipboard_get_text()

        assert result == test_text
        assert len(result) == 10000

        # Restore original
        backend.clipboard_set_text(original)


class TestMacOSFocusWindow:
    """Test window focus operations."""

    def test_focus_window_with_valid_handle(self) -> None:
        """Test focusing a window with valid handle."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        windows = backend.list_windows(visible_only=True)

        if len(windows) < 1:
            pytest.skip("Need at least one window for testing")

        # Focus should not raise for valid handle
        handle = windows[0].handle
        backend.focus_window(handle)

    def test_focus_window_with_invalid_handle(self) -> None:
        """Test focusing a window with invalid handle."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Invalid handle should not raise, just do nothing
        backend.focus_window(999999999)


class TestMacOSPermissionCheck:
    """Test permission checking methods."""

    def test_check_permissions_structure(self) -> None:
        """Test that check_permissions returns correct structure."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        try:
            perms = backend.check_permissions()

            # Should have all expected keys
            assert "mouse" in perms
            assert "keyboard" in perms
            assert "window" in perms
            assert "accessibility" in perms
            assert "screen_recording" in perms

            # All values should be boolean
            assert isinstance(perms["mouse"], bool)
            assert isinstance(perms["keyboard"], bool)
            assert isinstance(perms["window"], bool)
            assert isinstance(perms["accessibility"], bool)
            assert isinstance(perms["screen_recording"], bool)

            # These should always be True
            assert perms["mouse"] is True
            assert perms["keyboard"] is True
            assert perms["window"] is True
            # screen_recording is False by default
            assert perms["screen_recording"] is False

        except AttributeError:
            # AXIsProcessTrusted might not be available in some environments
            pytest.skip("Permission check API not available")
