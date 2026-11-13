import os
from pathlib import Path

from dotenv import load_dotenv

# .parent -> gmgf/   .parent.parent -> goodmorning-to-gf/ (project root)
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

PROFILE_DIR = BASE_DIR / "profile"
STATE_FILE = BASE_DIR / "state.json"

PHONE = os.getenv("WHATSAPP_PHONE")

MESSAGES = [
    "Bom dia, meu amor! Que o teu dia seja lindo ❤️",
    "Bom dia! Já estou com saudades tuas 😘",
    "Bom diaaa meu docinho de CU"

]

MAX_DELAY_SECONDS = int(os.getenv("MAX_DELAY_SECONDS"))
PAGE_LOAD_TIMEOUT_MS = int(os.getenv("PAGE_LOAD_TIMEOUT_MS"))