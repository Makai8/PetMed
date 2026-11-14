"""Settings for the PetMed API, read from src/.env (never committed)."""
import os

from dotenv import load_dotenv

# Load src/.env no matter which folder the server is started from.
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

DB_ENGINE = os.getenv("DB_ENGINE", "mysql")  # "mysql" for the team; "sqlite" only for offline tests
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "petmed")
DB_PATH = os.getenv("DB_PATH", "")  # only used when DB_ENGINE=sqlite

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
TOKEN_MAX_AGE_SECONDS = int(os.getenv("TOKEN_MAX_AGE_SECONDS", str(8 * 60 * 60)))  # 8 hours
