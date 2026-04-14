#!/usr/bin/env python3
"""
screenshot.py — モバイル端末向け高画質フルページスクリーンショット

Usage:
    python screenshot.py <html-path> [options]

Options:
    --output <path>     出力先（デフォルト: HTML と同名 .png）
    --width <px>        viewport 幅（デフォルト: 390）
    --scale <n>         deviceScaleFactor（デフォルト: 3）
    --browser <path>    ブラウザ実行パスを手動指定
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from platform import system


# ---------------------------------------------------------------------------
# ブラウザ自動検出（多層検出）
# ---------------------------------------------------------------------------

# PATH 検索用の実行ファイル名（優先順）
_WHICH_NAMES = ["msedge", "google-chrome-stable", "google-chrome", "chromium-browser", "chromium"]

# フォールバック: 既知のインストールパス（PATH に登録されていない場合用）
_KNOWN_PATHS: dict[str, list[str]] = {
    "Darwin": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ],
}


def _detect_from_path() -> str | None:
    """PATH 環境変数からブラウザを検出する。Linux やカスタムインストールに有効。"""
    for name in _WHICH_NAMES:
        found = shutil.which(name)
        if found:
            return found
    return None


def _detect_from_registry() -> str | None:
    """Windows レジストリからブラウザのインストールパスを検出する。"""
    if system() != "Windows":
        return None
    try:
        import winreg
    except ImportError:
        return None

    # App Paths レジストリキー（標準的なインストーラが登録する）
    app_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"),
    ]
    for hive, key_path in app_keys:
        try:
            with winreg.OpenKey(hive, key_path) as key:
                value, _ = winreg.QueryValueEx(key, None)  # デフォルト値 = 実行パス
                if value and Path(value).exists():
                    return value
        except OSError:
            continue
    return None


def _detect_from_known_paths() -> str | None:
    """既知のインストールパスからブラウザを検出する（macOS フォールバック用）。"""
    os_name = system()
    for p in _KNOWN_PATHS.get(os_name, []):
        if Path(p).exists():
            return p
    return None


def detect_browser() -> str | None:
    """ローカルにインストールされた Chromium 系ブラウザを検出する。

    検出順序:
      1. PATH 環境変数（shutil.which）
      2. Windows レジストリ（App Paths）
      3. 既知のインストールパス（macOS /Applications 等）
    """
    return _detect_from_path() or _detect_from_registry() or _detect_from_known_paths()


# ---------------------------------------------------------------------------
# メイン処理
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="モバイル端末向け高画質フルページスクリーンショット"
    )
    parser.add_argument("html_path", help="HTML ファイルのパス")
    parser.add_argument("--output", help="出力 PNG パス（デフォルト: HTML と同名 .png）")
    parser.add_argument("--width", type=int, default=390, help="viewport 幅 (デフォルト: 390)")
    parser.add_argument("--scale", type=int, default=3, help="deviceScaleFactor (デフォルト: 3)")
    parser.add_argument("--browser", help="ブラウザ実行パスを手動指定")
    args = parser.parse_args()

    # HTML ファイルの存在確認
    html_file = Path(args.html_path).resolve()
    if not html_file.exists():
        print(f"Error: HTML file not found: {html_file}", file=sys.stderr)
        sys.exit(1)

    # 出力パス
    output_path = Path(args.output) if args.output else html_file.with_suffix(".png")

    # Playwright 自動インストール
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not found. Installing...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        from playwright.sync_api import sync_playwright

    # ブラウザ検出
    browser_path = args.browser or detect_browser()

    with sync_playwright() as pw:
        # ブラウザ起動
        launch_args = ["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"]

        if browser_path:
            print(f"Browser: {browser_path}", file=sys.stderr)
            browser = pw.chromium.launch(
                executable_path=browser_path,
                headless=True,
                args=launch_args,
            )
        else:
            # ローカルブラウザなし → Playwright 内蔵ブラウザにフォールバック
            print(
                "No local browser detected. Falling back to bundled browser...",
                file=sys.stderr,
            )
            try:
                browser = pw.chromium.launch(headless=True, args=launch_args)
            except Exception:
                # 内蔵ブラウザ未ダウンロード → 自動インストール
                print("Bundled browser not found. Installing chromium...", file=sys.stderr)
                subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
                browser = pw.chromium.launch(headless=True, args=launch_args)

        try:
            page = browser.new_page(
                viewport={"width": args.width, "height": 844},
                device_scale_factor=args.scale,
            )

            # file:// プロトコルで HTML を開く
            file_url = html_file.as_uri()
            page.goto(file_url, wait_until="networkidle", timeout=30000)

            # フルページスクリーンショット
            page.screenshot(path=str(output_path), full_page=True, type="png")

            # 成功 → stdout にパスを出力
            print(str(output_path))
        finally:
            browser.close()


if __name__ == "__main__":
    main()
