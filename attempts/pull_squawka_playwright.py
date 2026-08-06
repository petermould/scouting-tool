"""
Uses a real (headless) Chrome browser via Playwright to load the Squawka
stats page and intercept the actual "statistics" API response - this uses
a genuine browser network stack, which can get past bot-detection that
blocked plain `requests` and `cloudscraper`.

Usage:
    python3 pull_squawka_playwright.py
"""
import json
from playwright.sync_api import sync_playwright

TARGET_URL = "https://www.squawka.com/en/stats/competitions/championship-2025-2026/"
captured_data = []


def handle_response(response):
    all_responses.append(response.url)
    if "wp-json/vcsw/v2/statistics" in response.url and response.request.method == "POST":
        try:
            data = response.json()
            captured_data.append(data)
            print(f"Captured response from {response.url}")
            print(f"  items count: {len(data.get('items', []))}")
        except Exception as e:
            print(f"  Could not parse response as JSON: {e}")


all_responses = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on("response", handle_response)

    print(f"Loading {TARGET_URL} ...")
    page.goto(TARGET_URL, wait_until="load", timeout=30000)
    page.wait_for_timeout(5000)

    # save a screenshot and the page title so we can see what actually loaded
    page.screenshot(path="squawka_debug.png", full_page=True)
    print(f"Page title: {page.title()}")

    browser.close()

print(f"\nTotal network responses seen: {len(all_responses)}")
print("Sample of URLs captured (first 20):")
for url in all_responses[:20]:
    print(f"  {url}")

if captured_data:
    with open("squawka_raw_response.json", "w") as f:
        json.dump(captured_data, f, indent=2)
    print(f"\nSaved {len(captured_data)} captured response(s) to squawka_raw_response.json")
else:
    print("\nNo matching API responses were captured - the page structure "
          "may differ from what we expect, or the request didn't fire.")