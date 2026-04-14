# share-this

[English](README.md) | [中文](README_zh.md)

AI との会話を、美しくシェアしやすい画像に。コマンドひとつで実現できます。

AI の会話内容を、洗練されたシェアしやすい HTML ページに変換する Claude Code スキルです。モバイル共有に最適化された高解像度のフルページ PNG スクリーンショットも自動生成します。

## 特徴

- **自己完結型 HTML** — インライン SVG ダイアグラムと CSS を含む単一ファイルで、外部依存はありません
- **自動スクリーンショット** — モバイルビューポート（390px、3 倍 Retina）でフルページ PNG を生成し、手軽にシェアできます
- **クロスプラットフォーム** — Windows、macOS、Linux 上の Edge、Chrome、Chromium を自動検出し、見つからない場合は Playwright 内蔵の Chromium にフォールバックします

## 利用シーン

| 利用シーン | 例 |
|---|---|
| 会話のインサイトを共有 | 調査結果、比較分析、意思決定のまとめ |
| 技術的な深掘り | パフォーマンスベンチマーク、アーキテクチャ設計 |
| インシデント振り返り | インシデント分析、根本原因の調査 |
| 学習のまとめ | 技術概念の整理、チュートリアルの振り返り |
| 提案と比較 | 新機能の提案、ツール比較 |

## インストール

### 1. Claude Code にスキルを追加

このフォルダを Claude Code のスキルディレクトリにコピーするか、そこにシンボリックリンクを作成します：

```bash
# 例：プロジェクトレベルのスキルに追加
cp -r share-this/share-this /path/to/your/project/.claude/skills/share-this

# またはユーザーレベルのスキルに追加
cp -r share-this/share-this ~/.claude/skills/share-this
```

### 2. 依存関係（自動インストール）

手動でセットアップする必要はありません。初回スクリーンショット時に、スクリプトが自動的にインストールします：

- `playwright`（Python パッケージ）— まだインストールされていない場合
- Chromium ブラウザ — ローカルに Edge または Chrome が検出されない場合のみ

## 使い方

Claude Code の会話中に、このスキルを呼び出します：

```text
/share-this
```

Claude が以下を実行します：

1. 現在の会話から重要なインサイトを抽出します
2. インライン SVG ダイアグラムを含む、構造化されたビジュアル HTML ページを生成します
3. モバイル最適化されたフルページスクリーンショット（PNG）を自動撮影
4. 2 つのファイルを保存し、保存先を通知します

## スクリーンショットスクリプト

スクリーンショットスクリプトは単体でも使用できます：

```bash
python scripts/screenshot.py <html-file> [options]
```

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| `--output <path>` | `<html-name>.png` | 出力 PNG パス |
| `--width <px>` | `390` | ビューポート幅 |
| `--scale <n>` | `3` | デバイススケールファクター（3 = Retina 3x） |
| `--browser <path>` | 自動検出 | ブラウザ実行ファイルのパス |

### ブラウザ検出

スクリプトは、インストール済みのブラウザを以下の順序で自動検出します：

| プラットフォーム | 検出順序 |
|---|---|
| Windows | Edge → Chrome（レジストリ + PATH 経由） |
| macOS | Chrome → Edge → Chromium（PATH + /Applications 経由） |
| Linux | chromium-browser → chromium → google-chrome-stable → google-chrome（PATH 経由） |

ローカルブラウザが見つからない場合は、Playwright 内蔵の Chromium がフォールバックとして使用されます。

## 出力

- **HTML** — 自己完結型で印刷にも対応し、インライン SVG ダイアグラムを含みます
- **PNG** — 幅 1170px（390 × 3 倍スケール）で、モバイル共有向けに最適化されています

## 例

![絵文字の歴史と豆知識](demo/emoji-history-and-fun-facts.png)

## ライセンス

[MIT](LICENSE)
