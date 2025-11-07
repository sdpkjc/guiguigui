# Release Guide

This document describes how to release a new version of PyGUI to PyPI.

## Prerequisites

### 1. PyPI Configuration

The project uses **Trusted Publishing** (recommended by PyPI), which doesn't require API tokens:

1. Go to https://pypi.org/manage/account/publishing/
2. Add a new pending publisher:
   - **PyPI Project Name**: `guiguigui`
   - **Owner**: `sdpkjc`
   - **Repository name**: `PyGUI`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`

For TestPyPI (optional, for testing):
1. Go to https://test.pypi.org/manage/account/publishing/
2. Add the same configuration with environment name: `testpypi`

### 2. Version Update

Update version in `pyproject.toml`:

```toml
[project]
name = "guiguigui"
version = "0.1.0"  # Update this
```

## Release Process

### Option 1: Automatic Release (Recommended)

1. **Update version** in `pyproject.toml`

2. **Update CHANGELOG** (optional but recommended):
   ```bash
   # Create CHANGELOG.md if it doesn't exist
   echo "# Changelog" > CHANGELOG.md
   echo "" >> CHANGELOG.md
   echo "## [0.1.0] - 2025-11-08" >> CHANGELOG.md
   echo "" >> CHANGELOG.md
   echo "### Added" >> CHANGELOG.md
   echo "- Initial release" >> CHANGELOG.md
   ```

3. **Commit changes**:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Release v0.1.0"
   ```

4. **Create and push tag**:
   ```bash
   git tag v0.1.0
   git push origin main
   git push origin v0.1.0
   ```

5. **GitHub Actions will automatically**:
   - Build the package
   - Run tests
   - Publish to PyPI
   - Create GitHub Release with artifacts

### Option 2: Test on TestPyPI First

1. Go to GitHub Actions: https://github.com/sdpkjc/PyGUI/actions/workflows/publish.yml

2. Click "Run workflow"

3. Check "Publish to TestPyPI instead of PyPI"

4. Click "Run workflow"

5. After successful test, follow Option 1 to release to PyPI

### Option 3: Manual Release

If you need to publish manually:

```bash
# Install dependencies
uv pip install build twine

# Build package
uv build

# Check package
twine check dist/*

# Upload to TestPyPI (test first)
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, backward compatible

Examples:
- `v0.1.0` - Initial release
- `v0.2.0` - Add Windows backend support
- `v0.2.1` - Fix mouse click bug
- `v1.0.0` - First stable release

## Pre-release Versions

For alpha/beta/rc releases:

```bash
# Alpha
git tag v0.2.0a1
git push origin v0.2.0a1

# Beta
git tag v0.2.0b1
git push origin v0.2.0b1

# Release Candidate
git tag v0.2.0rc1
git push origin v0.2.0rc1
```

## Post-Release Checklist

After release:

- [ ] Verify package on PyPI: https://pypi.org/project/guiguigui/
- [ ] Test installation: `pip install guiguigui`
- [ ] Check GitHub Release: https://github.com/sdpkjc/PyGUI/releases
- [ ] Update documentation if needed
- [ ] Announce release (Twitter, Reddit, etc.)

## Troubleshooting

### Build Fails

Check that:
- Version in `pyproject.toml` is updated
- All tests pass: `uv run pytest`
- Code quality checks pass: `uv run ruff check .`

### PyPI Upload Fails

Common issues:
- **Version already exists**: Increment version number
- **Trusted Publishing not configured**: See Prerequisites section
- **Invalid distribution**: Run `twine check dist/*`

### GitHub Release Fails

- Ensure tag starts with `v` (e.g., `v0.1.0`)
- Check GitHub Actions logs for details

## Rollback

If you need to remove a bad release:

1. **DO NOT delete from PyPI** (versions are immutable)
2. Instead, release a new patch version with fixes
3. Mark the bad release as "yanked" on PyPI (optional)

```bash
# Yank a release (makes it hidden but still available)
pip install twine
twine upload --repository pypi --skip-existing dist/*
# Then go to PyPI web interface to yank the version
```

## Reference

- PyPI Trusted Publishing: https://docs.pypi.org/trusted-publishers/
- Python Packaging Guide: https://packaging.python.org/
- GitHub Actions: https://docs.github.com/en/actions
