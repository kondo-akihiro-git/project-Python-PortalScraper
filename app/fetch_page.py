# app/fetch_page.py
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

def format_text(text: str) -> str:
    # タブと半角スペースのみ削除（全角スペースは残す）
    return text.replace("\t", "").replace(" ", "")

def fetch_page(session, base_url, basic_id, basic_pass, logger, member_no, year_month, week_num):
    """
    指定週の週報ページを取得し、作業内容・学習内容・コメントを抽出して返す
    """
    logger.info("fetch weekly report")

    url = build_url(base_url, member_no, year_month, week_num)
    html = fetch_html(session, url, basic_id, basic_pass)

    # HTML解析してデータ抽出
    weekly_data = extract_weekly_data(html)
    learning_data = extract_learning_data(html)
    comment_data = extract_comment_data(html)

    return {
        "weekly": weekly_data,
        "learning": learning_data,
        "comment": comment_data,
    }

# HTMLページ取得
def fetch_html(session, url, bid, bpw):
    res = session.get(url, auth=HTTPBasicAuth(bid, bpw))
    res.raise_for_status()
    return res.text

# 「作業内容」を抽出
def extract_weekly_data(html):
    soup = BeautifulSoup(html, "html.parser")
    data = []

    table = soup.find("table", id="weekly_report_list")
    if not table:
        return data

    for tr in table.find("tbody").find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 4:
            continue

        day = tds[0].get_text(strip=True)
        div = tds[3].find("div", class_="readonly_area")
        content = format_text(div.get_text(separator="")) if div else ""
        data.append({"day": day, "content": content})

    return data

# 「直近で学んだこと、覚えたこと」を抽出
def extract_learning_data(html):
    soup = BeautifulSoup(html, "html.parser")
    data = ""

    target_div = None
    for div in soup.find_all("div"):
        if div.get_text(strip=True).startswith("直近で学んだこと"):
            target_div = div
            break

    if target_div:
        content = target_div.find("div", class_="readonly_area")
        if content:
            data = format_text(content.get_text(separator=""))

    return data

# 「コメント欄」を抽出
def extract_comment_data(html):
    soup = BeautifulSoup(html, "html.parser")
    data = ""

    target_div = None
    for div in soup.find_all("div"):
        if div.get_text(strip=True).startswith("コメント欄"):
            target_div = div
            break

    if target_div:
        content = target_div.find("div", class_="readonly_area")
        if content:
            data = format_text(content.get_text(separator=""))

    return data

def build_url(base_url: str, member_no: int, year_month: str, week_num: int, display: int = 1) -> str:
    """
    get_weekから取得した週情報を使ってURLを作成
    """
    return (
        f"{base_url}/weekly_report"
        f"?member_no={member_no}"
        f"&weekly_report_year_month={year_month}"
        f"&weekly_report_week_num={week_num}"
        f"&display={display}"
    )
