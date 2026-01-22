# app/main.py
import requests
from config import (
    BASE_URL,
    BASIC_AUTH_ID,
    BASIC_AUTH_PASS,
    LOGIN_ID,
    LOGIN_PASS,
    MEMBER_NO,
)
from logger import setup_logger
from auth_basic import access_with_basic_auth
from auth_login import login
from fetch_page import fetch_page
from set_values import set_values
from get_week import get_week


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

    # 現在のページから週情報を取得
    week = get_week(
        session,
        BASE_URL,
        BASIC_AUTH_ID,
        BASIC_AUTH_PASS,
        logger,
    )

    # 週情報からページをfetch
    data = fetch_page(
        session,
        BASE_URL,
        BASIC_AUTH_ID,
        BASIC_AUTH_PASS,
        logger,
        member_no=MEMBER_NO,
        year_month=week[0],
        week_num=week[1]
    )

    # fetchしたページデータを渡す
    set_values(
        session,
        BASE_URL,
        BASIC_AUTH_ID,
        BASIC_AUTH_PASS,
        logger,
        data
    )

    logger.info("処理正常終了")


if __name__ == "__main__":
    main()
