import argparse
import json
import random
import time
from playwright.sync_api import sync_playwright

from .config import STATE_FILE, MESSAGES, PROFILE_DIR, PAGE_LOAD_TIMEOUT_MS


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=4), encoding="utf-8"
    )


def pick_message(last_message: str | None) -> str:
    """Pick a random message, avoiding the one sent last time."""
    options = [m for m in MESSAGES if m != last_message] or MESSAGES
    return random.choice(options)


def open_context(playwright):
    # Visible window (not headless) and a persistent profile with the saved login.
    return playwright.chromium.launch_persistent_context(
        str(PROFILE_DIR), headless=False
    )


def login() -> None:
    with sync_playwright() as p:
        context = open_context(p)
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://web.whatsapp.com")
        input("Scan the QR code, wait for your chats to load, then press Enter here... ")
        context.close()
    print("Login saved in the profile folder.")


def send(phone: str, message: str, dry_run: bool) -> bool:
    """Open the chat, type the message and (unless dry_run) send it."""
    with sync_playwright() as p:
        context = open_context(p)
        try:
            page = context.pages[0] if context.pages else context.new_page()
            page.goto(f"https://web.whatsapp.com/send?phone={phone}")

            # If you are not logged in, the QR code shows up and this times out.
            box = page.locator('footer div[contenteditable="true"]')
            box.wait_for(timeout=PAGE_LOAD_TIMEOUT_MS)
            box.click()

            # Type key by key, with small random pauses, instead of pasting.
            for char in message:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.05, 0.18))

            if dry_run:
                print("Dry run: message typed but not sent.")
                time.sleep(3)
                return False

            time.sleep(random.uniform(0.5, 1.5))
            page.keyboard.press("Enter")
            time.sleep(5)  # give WhatsApp time to actually send it
            return True
        finally:
            context.close()
