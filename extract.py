import json
import re
import subprocess
import sys
from pathlib import Path


URL = "https://apkcombo.com/instagram/com.instagram.android/download/apk"
DATA_DIR = Path("data")


def download_html() -> str:
    result = subprocess.run(
        [
            "curl",
            "-L",
            "--fail",
            "--silent",
            "--show-error",
            "--compressed",
            "-A",
            "Mozilla/5.0",
            URL,
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        print("Failed to download APKCombo page.")
        print(result.stderr)
        sys.exit(1)

    return result.stdout


def detect_version(html: str) -> str:
    match = re.search(
        r'<meta name="description" content="[^"]*Version:\s*([0-9.]+)',
        html,
    )

    if not match:
        print("Could not detect current Instagram version.")
        sys.exit(1)

    return match.group(1)


def extract_version_codes(
    html: str,
    version: str,
) -> list[str]:
    pattern = re.compile(
        rf'<span class="vername">Instagram\s+'
        rf'{re.escape(version)}</span>\s*'
        rf'<span class="vercode">\((\d+)\)</span>',
        re.DOTALL,
    )

    version_codes = pattern.findall(html)

    return sorted(
        set(version_codes),
        key=int,
    )


def save_json(
    version: str,
    version_codes: list[str],
) -> Path:
    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = DATA_DIR / f"instagram-{version}.json"

    data = {
        "version_codes": version_codes,
    }

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )

        file.write("\n")

    return output_path


def main() -> None:
    html = download_html()

    version = detect_version(html)

    print(f"Detected version: {version}")

    version_codes = extract_version_codes(
        html,
        version,
    )

    if not version_codes:
        print("No versionCodes found.")
        sys.exit(1)

    print(f"VersionCodes found: {len(version_codes)}")

    for version_code in version_codes:
        print(version_code)

    output_path = save_json(
        version,
        version_codes,
    )

    print()
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
