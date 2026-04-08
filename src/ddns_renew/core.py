import sys
from urllib.parse import urlparse
import os
from playwright.sync_api import (
    sync_playwright,
    ProxySettings,
    TimeoutError as PlaywrightTimeoutError,
)
from playwright_recaptcha import recaptchav2


def confirm_host(host_id, proxy_url=None):
    target_url = f"https://www.noip.com/confirm-host?n={host_id}"

    # Parse the proxy URL into Playwright's required dictionary format
    proxy_settings: ProxySettings | None = None

    if proxy_url:
        parsed_proxy = urlparse(proxy_url)
        proxy_settings = {
            "server": f"{parsed_proxy.scheme}://{parsed_proxy.hostname}:{parsed_proxy.port}"
        }
        if parsed_proxy.username:
            proxy_settings["username"] = parsed_proxy.username
        if parsed_proxy.password:
            proxy_settings["password"] = parsed_proxy.password
        print(f"Using Proxy: {proxy_settings['server']}")

    # Check environment for HEADLESS toggle (Defaults to True)
    headless_mode = os.environ.get("HEADLESS", "True").lower() == "true"

    # Track success state for a graceful exit
    success = False

    with sync_playwright() as p:
        # Launch Chromium with the proxy settings and headless toggle
        browser = p.chromium.launch(headless=headless_mode, proxy=proxy_settings)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print(f"Navigating to {target_url} (Initial Load)")
            page.goto(target_url, wait_until="networkidle")

            # --- BYPASS UPSELL LOGIC ---
            print("Allowing No-IP to register session state...")
            page.wait_for_timeout(2000)

            print("Reloading to bypass the upsell page...")
            page.reload(wait_until="networkidle")
            # ---------------------------

            print("Waiting for reCAPTCHA and attempting to solve...")
            try:
                with recaptchav2.SyncSolver(page) as solver:
                    solver.solve_recaptcha(wait=True)
                print("reCAPTCHA solved successfully.")
            except Exception as e:
                print(f"reCAPTCHA solving failed or timed out: {e}")
                # We log the error but continue, just in case the button is still clickable.

            # Find the button by its exact text
            submit_button = page.locator('button:has-text("Confirm your hostname now")')

            # Click the button
            print("Submitting the form...")
            submit_button.click()

            # Look for the success header that appears on the next page
            success_message = page.locator('h1:has-text("Update Successful")')

            try:
                # Wait up to 15 seconds for the success message to appear
                success_message.wait_for(state="visible", timeout=15000)
                print("Success! Host confirmed.")
                success = True
            except PlaywrightTimeoutError:
                print("Failed to confirm host or timed out waiting for success page.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            # Gracefully close the browser context before exiting Python
            browser.close()

    # Exit with the proper status code after Playwright has cleanly shut down
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
