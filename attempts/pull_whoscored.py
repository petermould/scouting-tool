"""
Uses a real Playwright-driven browser to load WhoScored's Championship
Passing player stats table and extract the rendered data.

Usage:
    python3 pull_whoscored.py
"""
from playwright.sync_api import sync_playwright
import pandas as pd

URL = "https://www.whoscored.com/regions/252/tournaments/7/seasons/10784/stages/24580/playerstatistics/england-championship-2025-2026"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print(f"Loading {URL} ...")
    page.goto(URL, wait_until="load", timeout=30000)
    page.wait_for_timeout(4000)

    print("Page title:", page.title())

    # click the "Passing" tab to switch the table view
    try:
        page.click("text=Passing", timeout=5000)
        page.wait_for_timeout(3000)
        print("Clicked Passing tab")
    except Exception as e:
        print(f"Could not click Passing tab: {e}")

    # take a screenshot so we can see what actually rendered
    page.screenshot(path="whoscored_debug.png", full_page=True)

    # try to find any table on the page and print its structure
    tables = page.query_selector_all("table")
    print(f"Found {len(tables)} <table> elements on the page")

    for i, table in enumerate(tables):
        rows = table.query_selector_all("tr")
        print(f"  Table {i}: {len(rows)} rows")

    browser.close()

print("\nCheck whoscored_debug.png to see what actually rendered")