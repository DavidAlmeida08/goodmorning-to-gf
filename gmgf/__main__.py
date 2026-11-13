import argparse
import random
import sys
import time
from datetime import date

from playwright.sync_api import TimeoutError as PlaywrightTimeout

from .config import MAX_DELAY_SECONDS, PHONE
from .gmgf import load_state, login, pick_message, save_state, send


def main() -> int:
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--login", action="store_true", help="scan the QR code once")
    parser.add_argument("--dry-run", action="store_true", help="type but do not send")
    args = parser.parse_args()

    # Login
    if args.login:
        login()
        return 0

    if not PHONE:
        print("Missing WHATSAPP_PHONE in .env (international format, digits only).")
        return 1

    state = load_state()
    today = date.today().isoformat()
    if not args.dry_run and state.get("last_sent_date") == today:
        print("Already sent today. Nothing to do.")
        return 0

    message = pick_message(state.get("last_message"))

    if not args.dry_run:
        delay = random.uniform(0, MAX_DELAY_SECONDS)
        print(f"Waiting {delay:.0f}s before sending...")
        time.sleep(delay)

    try:
        sent = send(PHONE, message, args.dry_run)
    except PlaywrightTimeout:
        print("The chat did not load. Not logged in (run --login) or no connection?")
        return 1

    if sent:
        state["last_sent_date"] = today
        state["last_message"] = message
        save_state(state)
        print("Message sent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

