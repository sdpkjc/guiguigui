# PyGUI

[![PyPI](https://img.shields.io/pypi/v/guiguigui.svg)](https://pypi.org/project/guiguigui/)
[![Tests](https://github.com/sdpkjc/PyGUI/workflows/Tests/badge.svg)](https://github.com/sdpkjc/PyGUI/actions)
[![Code Quality](https://github.com/sdpkjc/PyGUI/workflows/Code%20Quality/badge.svg)](https://github.com/sdpkjc/PyGUI/actions)
[![codecov](https://codecov.io/gh/sdpkjc/PyGUI/branch/main/graph/badge.svg)](https://codecov.io/gh/sdpkjc/PyGUI)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A minimalist cross-platform GUI automation library for Python.

## Features

- **Cross-platform** - macOS, Linux (X11/Wayland), Windows
- **Complete GUI control** - Mouse, keyboard, window, display, clipboard
- **Multi-monitor support** - Full multi-display and high-DPI handling
- **Powerful macro system** - Easy automation with action-based macros
- **Clean design** - No image matching or OCR bloat

## Installation

```bash
# Using uv (recommended)
uv pip install guiguigui

# macOS
uv pip install "guiguigui[macos]"

# Linux
uv pip install "guiguigui[linux]"

# Using pip
pip install guiguigui
pip install "guiguigui[macos]"  # macOS
pip install "guiguigui[linux]"  # Linux
```

## Quick Start

```python
from pygui import mouse, keyboard, display, window, clipboard

# Mouse operations
mouse.move(500, 300)
mouse.click()
mouse.drag(700, 400, duration=0.5)

# Keyboard operations
keyboard.type("Hello, PyGUI!")
keyboard.hotkey("cmd", "s")  # macOS
keyboard.hotkey("ctrl", "s")  # Windows/Linux

# Clipboard
clipboard.set("Copy this text")
text = clipboard.get()

# Display information
for d in display.list():
    print(f"{d.name}: {d.bounds.width}x{d.bounds.height}")

# Window management
windows = window.find(title="Chrome")
if windows:
    window.focus(windows[0])
```

## Macro System

```python
from pygui.core.macro import Macro, MouseMove, MouseClick, KeyWrite

macro = (
    Macro("auto_login")
    .add(MouseMove(300, 200, 0.2))
    .add(MouseClick())
    .add(KeyWrite("username"))
    .wait(0.1)
    .add(MouseMove(300, 250, 0.2))
    .add(MouseClick())
    .add(KeyWrite("password"))
)

macro.run()
```

## API Overview

| Module | Key Functions |
|--------|--------------|
| **mouse** | `position()`, `move()`, `click()`, `drag()`, `scroll()` |
| **keyboard** | `press()`, `release()`, `type()`, `hotkey()` |
| **display** | `list()`, `primary()`, `at()`, `virtual_screen_rect()` |
| **window** | `list()`, `active()`, `find()`, `focus()`, `move()`, `resize()` |
| **clipboard** | `get()`, `set()`, `clear()`, `has_text()` |

## Testing

```bash
# Run unit tests
uv run pytest tests/unit/ -v

# Run with coverage
uv run pytest tests/unit/ --cov=pygui --cov-report=html

# Run integration tests (requires GUI environment)
uv run pytest tests/integration/ -v -m integration
```

See [TESTING.md](TESTING.md) for detailed testing documentation.

## Development

```bash
git clone https://github.com/sdpkjc/PyGUI.git
cd PyGUI
uv sync --extra dev --extra macos

# Code quality
uv run ruff check pygui
uv run mypy pygui

# Pre-commit hooks
uv run pre-commit run --all-files
```

For detailed development guide, see:
- [DESIGN.md](DESIGN.md) - Architecture and design decisions
- [CLAUDE.md](CLAUDE.md) - Development setup and common tasks
- [TODO.md](TODO.md) - Development roadmap and pending tasks
- [TESTING.md](TESTING.md) - Testing guide and infrastructure
- [RELEASING.md](RELEASING.md) - Release process and PyPI publishing

## Platform Notes

| Platform | Status | Notes |
|----------|--------|-------|
| **macOS** | ✅ Full support | Requires accessibility permissions |
| **Linux (X11)** | 🚧 Planned | Requires `python-xlib` |
| **Linux (Wayland)** | ⚠️ Limited | Security restrictions apply |
| **Windows** | 🚧 Planned | No extra dependencies (uses ctypes) |

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Links

- **Documentation**: [DESIGN.md](DESIGN.md), [TESTING.md](TESTING.md)
- **Issues**: https://github.com/sdpkjc/PyGUI/issues
- **Pull Requests**: https://github.com/sdpkjc/PyGUI/pulls
