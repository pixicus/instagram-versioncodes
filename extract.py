import re
import subprocess
import sys


VERSION = "443.0.0.48.82"
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


def extract_version_codes(html: str) -> dict[str, list[str]]:
    architecture_pattern = re.compile(
        r"<code>([^<]+)</code>(.*?)(?=<code>|$)",
        re.DOTALL,
    )

    version_pattern = re.compile(
        rf'<span class="vername">Instagram\s+'
        rf'{re.escape(VERSION)}</span>\s*'
        rf'<span class="vercode">\((\d+)\)</span>',
        re.DOTALL,
    )

    results: dict[str, list[str]] = {}

    for architecture_match in architecture_pattern.finditer(html):
        architecture = architecture_match.group(1).strip()
        section_html = architecture_match.group(2)

        version_codes = version_pattern.findall(section_html)

        if not version_codes:
            continue

        results[architecture] = sorted(
            set(version_codes),
            key=int,
        )

    return results


def main() -> None:
    html = download_html()

    print(f"Downloaded HTML: {len(html)} bytes")
    print(f"Version: {VERSION}")
    print()

    results = extract_version_codes(html)

    if not results:
        print("No versionCodes found.")
        sys.exit(1)

    total = 0

    for architecture, version_codes in results.items():
        print(f"{architecture}:")

        for version_code in version_codes:
            print(f"  {version_code}")

        print()

        total += len(version_codes)

    print(f"Total versionCodes: {total}")


if __name__ == "__main__":
    main()
