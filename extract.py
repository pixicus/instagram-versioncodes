import re
import subprocess
import sys


URL = "https://apkcombo.com/instagram/com.instagram.android/download/apk"


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


if __name__ == "__main__":
    main()
