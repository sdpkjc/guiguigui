from __future__ import annotations

import sys
import time

import pytest

from guiguigui import keyboard
from guiguigui.core.types import Key


@pytest.mark.integration
class TestKeyboardOperations:
    @pytest.mark.skip(reason="keyboard.is_pressed() not reliable in CI environment")
    def test_key_press_release(self) -> None:
        keyboard.press(Key.SHIFT)
        time.sleep(0.05)
        assert keyboard.is_pressed(Key.SHIFT)
        keyboard.release(Key.SHIFT)
        time.sleep(0.05)
        assert not keyboard.is_pressed(Key.SHIFT)

    def test_key_tap(self) -> None:
        keyboard.tap(Key.SPACE)
        time.sleep(0.1)

    def test_keyboard_layout(self) -> None:
        layout = keyboard.layout()
        assert isinstance(layout, str)
        assert len(layout) > 0

    def test_type_text_ascii(self) -> None:
        keyboard.type("hello", interval=0.01)
        time.sleep(0.1)

    @pytest.mark.skipif(
        sys.platform.startswith("linux"), reason="Unicode typing not yet implemented for X11"
    )
    def test_type_text_unicode(self) -> None:
        keyboard.type("你好", interval=0.01)
        time.sleep(0.1)

    def test_hotkey(self) -> None:
        keyboard.hotkey(Key.CTRL, "c", interval=0.01)
        time.sleep(0.1)

    @pytest.mark.skip(reason="keyboard.is_pressed() not reliable in CI environment")
    def test_modifier_keys(self) -> None:
        modifiers = [Key.SHIFT, Key.CTRL, Key.ALT]
        for mod in modifiers:
            keyboard.press(mod)
            time.sleep(0.05)
            assert keyboard.is_pressed(mod)
            keyboard.release(mod)
            time.sleep(0.05)
            assert not keyboard.is_pressed(mod)

    def test_function_keys(self) -> None:
        keyboard.tap(Key.F1)
        time.sleep(0.05)
        keyboard.tap(Key.F12)
        time.sleep(0.05)

    def test_special_keys(self) -> None:
        special_keys = [Key.ENTER, Key.TAB, Key.ESC, Key.BACKSPACE]
        for key in special_keys:
            keyboard.tap(key)
            time.sleep(0.05)

    def test_arrow_keys(self) -> None:
        arrow_keys = [Key.LEFT, Key.RIGHT, Key.UP, Key.DOWN]
        for key in arrow_keys:
            keyboard.tap(key)
            time.sleep(0.05)
