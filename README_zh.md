# share-this

[English](README.md) | [日本語](README_ja.md)

一条命令，即可将 AI 对话变成精美、便于分享的长图。

这是一个 Claude Code 技能，可将 AI 对话内容转换为精美、便于分享的 HTML 页面，并自动生成适合移动端分享的高清全页 PNG 长图。

## 特性

- **自包含 HTML** — 单文件内嵌 SVG 图表和 CSS，无需任何外部依赖
- **自动截图** — 以移动端视口（390px，3 倍 Retina）生成全页 PNG，便于分享
- **跨平台** — 自动检测 Windows、macOS 和 Linux 上的 Edge、Chrome 或 Chromium；若未找到，则回退到 Playwright 内置的 Chromium

## 使用场景

| 使用场景 | 示例 |
|---|---|
| 分享对话洞察 | 调研结果、对比分析、决策总结 |
| 技术深度探讨 | 性能基准测试、架构设计 |
| 事故复盘 | 事故分析、根因排查 |
| 学习总结 | 技术概念梳理、教程回顾 |
| 方案与比较 | 新功能提案、工具对比 |

## 安装

### 1. 将技能添加到 Claude Code

将此文件夹复制到 Claude Code 的技能目录中，或在其中创建指向它的符号链接：

```bash
# 示例：添加到项目级技能
cp -r share-this/share-this /path/to/your/project/.claude/skills/share-this

# 或添加到用户级技能
cp -r share-this/share-this ~/.claude/skills/share-this
```

### 2. 依赖（自动安装）

无需手动配置。首次截图时，脚本会自动安装：

- `playwright`（Python 包）— 如果尚未安装
- Chromium 浏览器 — 仅在未检测到本地 Edge 或 Chrome 时安装

## 使用方法

在任意 Claude Code 对话中调用该技能：

```text
/share-this
```

Claude 将会：

1. 从当前对话中提取关键洞察
2. 生成结构化、可视化的 HTML 页面，内嵌 SVG 图表
3. 自动截取移动端优化的全页截图（PNG）
4. 保存这两个文件，并告知存储位置

## 截图脚本

截图脚本也可以独立使用：

```bash
python scripts/screenshot.py <html-file> [options]
```

### 选项

| 选项 | 默认值 | 说明 |
|---|---|---|
| `--output <path>` | `<html-name>.png` | 输出 PNG 路径 |
| `--width <px>` | `390` | 视口宽度 |
| `--scale <n>` | `3` | 设备缩放比（3 = Retina 3x） |
| `--browser <path>` | 自动检测 | 浏览器可执行文件路径 |

### 浏览器检测

脚本会按以下顺序自动检测已安装的浏览器：

| 平台 | 检测顺序 |
|---|---|
| Windows | Edge → Chrome（通过注册表 + PATH） |
| macOS | Chrome → Edge → Chromium（通过 PATH + /Applications） |
| Linux | chromium-browser → chromium → google-chrome-stable → google-chrome（通过 PATH） |

如果未找到本地浏览器，则会使用 Playwright 内置的 Chromium 作为后备方案。

## 输出

- **HTML** — 自包含、适合打印，且内嵌 SVG 图表
- **PNG** — 宽 1170px（390 × 3 倍缩放），适合在移动端分享

## 示例

![Emoji 的历史与趣闻](demo/emoji-history-and-fun-facts.png)

## 许可证

[MIT](LICENSE)
