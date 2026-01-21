import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

BASIC_AUTH_ID = os.getenv("BASIC_AUTH_ID")
BASIC_AUTH_PASS = os.getenv("BASIC_AUTH_PASS")

LOGIN_ID = os.getenv("LOGIN_ID")
LOGIN_PASS = os.getenv("LOGIN_PASS")
