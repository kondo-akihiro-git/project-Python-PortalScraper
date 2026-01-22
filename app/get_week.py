# app/get_week.py
import calendar
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# テストデータ定義

def get_week(session, url, basic_id, basic_pass, logger):
    url = build_url(url)
    html = fetch_html(session, url, basic_id, basic_pass)
    year_month, week_num = search_current_week(html)
    logger.info(f"現在の週情報: 年月={year_month}, 週番号={week_num}")

    prev_year_month, prev_week_num = get_previous_week(year_month, week_num)
    logger.info(f"1週前の週情報: 年月={prev_year_month}, 週番号={prev_week_num}")
    return prev_year_month, prev_week_num


def fetch_html(session, url, bid, bpw):
    res = session.get(url, auth=HTTPBasicAuth(bid, bpw))
    res.raise_for_status()
    return res.text

def search_current_week(html):
    soup = BeautifulSoup(html, "html.parser")

    # 年月
    year_month_input = soup.find("input", id="weekly_report_year_month")
    if not year_month_input or not year_month_input.get("value"):
        raise RuntimeError("weekly_report_year_month input not found or empty")
    year_month = year_month_input["value"].strip()

    # 週番号
    week_select = soup.find("select", id="weekly_report_week_num")
    if not week_select:
        raise RuntimeError("weekly_report_week_num select not found")

    selected_option = week_select.find("option", selected=True)
    if not selected_option or not selected_option.get("value"):
        raise RuntimeError("selected week option not found")
    week_num = int(selected_option["value"].strip())

    print(year_month, week_num)
    return year_month, week_num

def get_previous_week(year_month: str, week_num: int):
    """
    指定された年-月と週番号から1週前の年月・週番号を返す
    - year_month: "YYYY-MM"
    - week_num: int (1~5)
    """
    if week_num > 1:
        # 同じ月内で前週
        return year_month, week_num - 1
    else:
        # 今週が1週目の場合 → 前月の最終週にする
        # 前月の年月を計算
        dt = datetime.strptime(year_month + "-01", "%Y-%m-%d")
        first_day_prev_month = dt.replace(day=1) - timedelta(days=1)
        prev_year_month = first_day_prev_month.strftime("%Y-%m")

        # 前月の最終週番号を取得（最大5週と仮定）
        prev_week_num = get_last_week_of_month(prev_year_month)
        return prev_year_month, prev_week_num


def get_last_week_of_month(year_month: str) -> int:
    year, month = map(int, year_month.split("-"))
    cal = calendar.Calendar(firstweekday=0)  # 月曜始まり
    month_weeks = cal.monthdayscalendar(year, month)
    # 空日(0)もあるけど、単純に週の数が最終週番号
    return len(month_weeks)


def build_url(base_url: str) -> str:
    """
    get_weekから取得した週情報を使ってURLを作成
    """
    return (
        f"{base_url}/weekly_report"
    )