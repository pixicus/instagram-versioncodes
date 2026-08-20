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

        try:
            response = page.goto(
                URL,
                wait_until="domcontentloaded",
                timeout=60_000,
            )

            print(
                f"HTTP status: "
                f"{response.status if response else 'unknown'}"
            )

        except Exception as exception:
            print(f"Navigation error: {exception}")

        print(f"Final URL: {page.url}")

        try:
            print(f"Title: {page.title()}")
        except Exception as exception:
            print(f"Title error: {exception}")

        # Lăsăm JavaScript-ul paginii să încarce conținutul dinamic.
        page.wait_for_timeout(10_000)

        try:
            body_text = page.locator("body").inner_text(
                timeout=10_000,
            )

            print(f"Body length: {len(body_text)}")
            print()
            print("===== PAGE TEXT =====")
            print(body_text[:8000])
            print("===== END PAGE TEXT =====")

        except Exception as exception:
            print(f"Body error: {exception}")

        try:
            page.screenshot(
                path="apkpure-debug.png",
                full_page=True,
                timeout=30_000,
            )

            print("Screenshot created.")

        except Exception as exception:
            print(f"Screenshot error: {exception}")

        browser.close()


if __name__ == "__main__":
    main()
