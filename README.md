# share-this

[中文](README_zh.md) | [日本語](README_ja.md)

Turn your AI conversations into beautiful, shareable images with a single command.

A Claude Code skill that turns AI conversations into polished HTML pages and high-resolution, mobile-ready full-page PNG screenshots.

## Features

- **Self-contained HTML** — A single file with inline SVG diagrams and CSS, with no external dependencies
- **Auto screenshots** — Full-page PNGs captured in a mobile viewport (390px at 3x Retina), ready for sharing
- **Cross-platform** — Automatically detects Edge, Chrome, or Chromium on Windows, macOS, and Linux. Falls back to Playwright's bundled Chromium if none are found

## Use Cases

| Use Case | Example |
|---|---|
| Share conversation insights | Research findings, comparative analysis, decision summaries |
| Technical deep-dives | Performance benchmarks, architecture design |
| Incident post-mortems | Incident analysis, root cause investigation |
| Learning summaries | Technical concept overviews, tutorial recaps |
| Proposals & comparisons | Feature proposals, tool comparisons |

## Installation

### 1. Add the skill to Claude Code

Copy this folder or symlink it into your Claude Code skills directory:

```bash
# Example: add to project-level skills
cp -r share-this/share-this /path/to/your/project/.claude/skills/share-this

# Or add to user-level skills
cp -r share-this/share-this ~/.claude/skills/share-this
```

### 2. Dependencies (auto-installed)

No manual setup is required. On the first screenshot, the script automatically installs:

- `playwright` (Python package) — if it is not already installed
- Chromium browser — only if no local Edge or Chrome is detected

## Usage

In any Claude Code conversation, invoke the skill:

```text
/share-this
```

Claude will:

1. Extract key insights from the current conversation
2. Generate a structured visual HTML page with inline SVG diagrams
3. Automatically capture a mobile-optimized full-page screenshot (PNG)
4. Save both files and tell you where they were written

## Screenshot Script

The screenshot script can also be used on its own:

```bash
python scripts/screenshot.py <html-file> [options]
```

### Options

| Option | Default | Description |
|---|---|---|
| `--output <path>` | `<html-name>.png` | Output PNG path |
| `--width <px>` | `390` | Viewport width |
| `--scale <n>` | `3` | Device scale factor (3 = Retina 3x) |
| `--browser <path>` | auto-detect | Browser executable path |

### Browser Detection

The script automatically detects installed browsers in this order:

| Platform | Detection Order |
|---|---|
| Windows | Edge → Chrome (via registry + PATH) |
| macOS | Chrome → Edge → Chromium (via PATH + /Applications) |
| Linux | chromium-browser → chromium → google-chrome-stable → google-chrome (via PATH) |

If no local browser is found, Playwright's bundled Chromium is used as a fallback.

## Output

- **HTML** — Self-contained, print-friendly output with inline SVG diagrams
- **PNG** — 1170px wide (390 x 3x scale), optimized for mobile sharing

## Example

![Emoji History and Fun Facts](demo/emoji-history-and-fun-facts.png)

## License

[MIT](LICENSE)
