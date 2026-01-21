import requests

from config import (
    BASE_URL,
    BASIC_AUTH_ID,
    BASIC_AUTH_PASS,
    LOGIN_ID,
    LOGIN_PASS,
)
from logger import setup_logger
from auth_basic import access_with_basic_auth
from auth_login import login
from fetch_page import fetch_top_page


def main():
    logger = setup_logger()
    session = requests.Session()

    logger.info("処理開始")

    access_with_basic_auth(
        session,
        BASE_URL,
        BASIC_AUTH_ID,
        BASIC_AUTH_PASS,
        logger,
    )

    login(
        session,
        BASE_URL,
        LOGIN_ID,
        LOGIN_PASS,
        BASIC_AUTH_ID,
        BASIC_AUTH_PASS,
        logger,
    )

    fetch_top_page(
        session,
        BASE_URL,
        BASIC_AUTH_ID,
        BASIC_AUTH_PASS,
        logger,
    )

    logger.info("処理正常終了")


if __name__ == "__main__":
    main()
