import argparse
import os


def parse_and_set_env():
    """Parse command line args and set corresponding environment variables"""
    parser = argparse.ArgumentParser(description="Your application")

    # Logging level group
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument("-q", action="store_true", help="Quiet mode")
    log_group.add_argument("-v", action="store_true", help="Verbose mode")

    # Database group
    db_group = parser.add_mutually_exclusive_group()
    db_group.add_argument("-s", action="store_true", help="SQLite database")
    db_group.add_argument("-p", action="store_true", help="Production database")

    # Mode group
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("-m", action="store_true", help="Mock services")
    mode_group.add_argument("-r", action="store_true", help="Real services")

    args = parser.parse_args()

    # Convert flags to environment variables
    os.environ["APP_LOG_LEVEL"] = (
        "quiet" if args.q else "verbose" if args.v else "normal"
    )
    os.environ["APP_DATABASE"] = "sqlite" if args.s else "production"
    os.environ["APP_MODE"] = "mock" if args.m else "production"

    return args


# Helper functions for easy access


def get_log_level():
    return os.getenv("APP_LOG_LEVEL", "normal")


def get_database():
    return os.getenv("APP_DATABASE", "production")


def get_mode():
    return os.getenv("APP_MODE", "production")


def is_quiet():
    return get_log_level() == "quiet"


def is_verbose():
    return get_log_level() == "verbose"


def is_sqlite():
    return get_database() == "sqlite"


def is_mock():
    return get_mode() == "mock"
