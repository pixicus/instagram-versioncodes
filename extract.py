import re

from playwright.sync_api import sync_playwright


VERSION = "443.0.0.48.82"

URL = "https://apkpure.net/instagram-app/com.instagram.android/download"


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
        )

        page = browser.new_page()

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60_000,
        )

        page.wait_for_timeout(3000)

        show_more_buttons = page.get_by_text(
            "Show More",
            exact=True,
        )

        count = show_more_buttons.count()

        print(f"Show More găsite: {count}")

        for index in range(count):
            try:
                show_more_buttons.nth(index).click()
                page.wait_for_timeout(1000)
            except Exception as exception:
                print(
                    f"Nu am putut apăsa Show More #{index}: "
                    f"{exception}"
                )

        page_text = page.locator("body").inner_text()

        pattern = rf"{re.escape(VERSION)}\s*\((\d+)\)"

        version_codes = sorted(
            set(re.findall(pattern, page_text)),
            key=int,
        )

        print()
        print(f"Versiune: {VERSION}")
        print(f"VersionCodes găsite: {len(version_codes)}")
        print()

        for version_code in version_codes:
            print(version_code)

        browser.close()


if __name__ == "__main__":
    main()
