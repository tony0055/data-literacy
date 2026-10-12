#!/usr/bin/env python3
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[4]
ENV_PATH = ROOT / ".env"
TARGET = "https://namu.wiki/w/%EC%98%81%EC%83%81%20%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5"


def load_env_value(path: Path, name: str) -> str:
    if not path.is_file():
        return ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == name:
            return value.strip().strip("'\"")
    return ""


def main() -> int:
    api_key = os.environ.get("FIRECRAWL_API_KEY") or load_env_value(
        ENV_PATH, "FIRECRAWL_API_KEY"
    )
    if not api_key:
        print("KEY_PRESENT=false")
        return 2

    if any(character in api_key for character in '\r\n"'):
        print("KEY_FORMAT_VALID=false")
        return 2

    payload = json.dumps(
        {
            "url": TARGET,
            "formats": ["markdown"],
            "onlyMainContent": True,
            "maxAge": 0,
        }
    )
    curl_config = "\n".join(
        [
            "silent",
            "show-error",
            'url = "https://api.firecrawl.dev/v2/scrape"',
            'request = "POST"',
            f'header = "Authorization: Bearer {api_key}"',
            'header = "Content-Type: application/json"',
        ]
    )

    try:
        completed = subprocess.run(
            ["curl", "--config", "-", "--data-binary", payload],
            input=curl_config,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if completed.returncode != 0:
            print(f"API_SUCCESS=false\nCURL_EXIT={completed.returncode}")
            return 1
        result = json.loads(completed.stdout)
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        print(f"API_SUCCESS=false\nERROR_TYPE={type(error).__name__}")
        return 1

    data = result.get("data") or {}
    metadata = data.get("metadata") or {}
    markdown = data.get("markdown") or ""
    print("KEY_PRESENT=true")
    print(f"API_SUCCESS={str(bool(result.get('success'))).lower()}")
    print(f"PAGE_STATUS={metadata.get('statusCode')}")
    print(f"PAGE_TITLE={metadata.get('title')}")
    print(f"MARKDOWN_CHARS={len(markdown)}")
    print(f"WAN_3_EXACT_MENTION={str('Wan 3.0' in markdown).lower()}")
    return 0 if result.get("success") and metadata.get("statusCode") == 200 else 1


if __name__ == "__main__":
    sys.exit(main())
