from guiguigui import clipboard, display, keyboard, mouse, window
from guiguigui.core.types import Key, MouseButton


def test_mouse():
    """Test mouse operations"""
    print("\n[Mouse Operations]")

    # Get current position
    pos = mouse.position()
    print(f"  Position: {pos}")

    # Move mouse
    mouse.move(pos.x + 50, pos.y + 50, duration=0.2)
    print(f"  Moved to: {mouse.position()}")

    # Click operations
    mouse.click()  # Left click
    mouse.click(MouseButton.RIGHT)  # Right click
    print("  Clicked: left, right")

    # Scroll
    mouse.scroll(dy=3)  # Scroll up
    print("  Scrolled up")

    # Context manager
    with mouse.pressed(MouseButton.LEFT):
        mouse.move_rel(10, 10, duration=0.1)
    print("  Drag completed")


def test_keyboard():
    """Test keyboard operations"""
    print("\n[Keyboard Operations]")

    # Type text (alias for write)
    keyboard.type("Hello")
    print("  Typed: Hello")

    # Press and release
    keyboard.press(Key.SHIFT)
    keyboard.tap(Key.A)
    keyboard.release(Key.SHIFT)
    print("  Pressed: Shift+A")

    # Hotkey
    keyboard.hotkey(Key.CMD, Key.A)  # Select all (macOS)
    print("  Hotkey: Cmd+A")

    # Context manager
    with keyboard.pressed(Key.SHIFT):
        keyboard.tap(Key.B)
    print("  Context: Shift+B")

    # Layout info
    print(f"  Keyboard layout: {keyboard.layout()}")


def test_display():
    """Test display operations"""
    print("\n[Display Operations]")

    # List all displays
    displays = display.list()
    print(f"  Displays: {len(displays)}")

    # Primary display
    primary = display.primary()
    print(f"  Primary: {primary.name} ({primary.bounds.width}x{primary.bounds.height})")

    # Display at point
    center_x = primary.bounds.width // 2
    center_y = primary.bounds.height // 2
    disp = display.at(center_x, center_y)
    if disp:
        print(f"  At center: {disp.name}")

    # Virtual screen
    virt = display.virtual_screen_rect()
    print(f"  Virtual screen: {virt.width}x{virt.height}")


def test_window():
    """Test window operations"""
    print("\n[Window Operations]")

    # List windows
    windows = window.list()
    print(f"  Total windows: {len(windows)}")

    # Active window
    active = window.active()
    if active:
        print(f"  Active: {active.title[:30]}...")

        # Window state
        state = window.get_state(active)
        print(f"  State: {state.value}")

    # Find window by title
    found = window.find(title="")
    if found:
        print(f"  Found: {found.title[:30]}...")

    # Window at position
    pos = mouse.position()
    win = window.at(pos.x, pos.y)
    if win:
        print(f"  At mouse: {win.title[:30]}...")


def test_clipboard():
    """Test clipboard operations"""
    print("\n[Clipboard Operations]")

    # Set and get (aliases)
    clipboard.set("GuiGuiGui Test")
    text = clipboard.get()
    print(f"  Clipboard: {text}")

    # Check if has text
    has_text = clipboard.has_text()
    print(f"  Has text: {has_text}")

    # Clear
    clipboard.clear()
    print(f"  After clear: {clipboard.has_text()}")

    # Restore
    clipboard.set(text)
    print("  Restored original")


def main():
    print("=" * 50)
    print("GuiGuiGui - Basic Operations Test")
    print("=" * 50)

    try:
        test_mouse()
        test_keyboard()
        test_display()
        test_window()
        test_clipboard()

        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        print("=" * 50)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
