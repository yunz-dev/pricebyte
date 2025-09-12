from config import is_quiet, is_verbose
from datetime import date, datetime


def log(string: str):
    if not is_quiet():
        print(f"LOG [{datetime.now()}]: {string}")


def detailed_log(string: str):
    if is_verbose():
        print(f"[{datetime.now()}]: {string}")
