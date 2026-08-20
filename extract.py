from playwright.sync_api import sync_playwright


URL = "https://apkpure.net/instagram-app/com.instagram.android/download"


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={
                "width": 1920,
                "height": 1080,
            }
        )

        response = page.goto(
            URL,
            wait_until="networkidle",
            timeout=90_000,
        )

        print(f"HTTP status: {response.status if response else 'unknown'}")
        print(f"Final URL: {page.url}")
        print(f"Title: {page.title()}")

        page.wait_for_timeout(5000)

        body_text = page.locator("body").inner_text()

        print(f"Body length: {len(body_text)}")
        print()
        print("===== PAGE TEXT =====")
        print(body_text[:5000])
        print("===== END PAGE TEXT =====")

        page.screenshot(
            path="apkpure-debug.png",
            full_page=True,
        )

        browser.close()


if __name__ == "__main__":
    main()
