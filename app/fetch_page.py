from requests.auth import HTTPBasicAuth
import os
from datetime import datetime
from bs4 import BeautifulSoup


def fetch_page(session, base_url, basic_id, basic_pass, logger):
    logger.info("fetch weekly report")

    url = (
        "https://eba-report.xyz/weekly_report"
        "?member_no=668"
        "&weekly_report_year_month=2026-01"
        "&weekly_report_week_num=3"
        "&display=1"
    )

    html = fetch_html(session, url, basic_id, basic_pass)
    save_txt(html)

# HTMLページ取得
def fetch_html(session, url, bid, bpw):
    res = session.get(url, auth=HTTPBasicAuth(bid, bpw))
    res.raise_for_status()
    return res.text

# ファイル保存
def save_txt(html):
    soup = BeautifulSoup(html, "html.parser")

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(base, "files")
    os.makedirs(out, exist_ok=True)

    ts = datetime.now().strftime("%m%d_%H%M%S")
    path = os.path.join(out, f"weekly_{ts}.txt")

    with open(path, "w", encoding="utf-8") as f:
        tbl = soup.find("table", id="weekly_report_list")
        if not tbl:
            return path

        for tr in tbl.find("tbody").find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) < 4:
                continue

            # 日付
            d = tds[0].get_text(strip=True)
            f.write(f"■日付:{d}\n")

            # 作業内容の抽出
            div = tds[3].find("div", class_="readonly_area")
            if div:
                raw = div.get_text(separator="")
                txt = format_text(raw)
                f.write(txt)

            f.write("\n\n" + "-" * 100 + "\n\n")

    return path

def format_text(text: str) -> str:
    # タブと半角スペースのみ削除（全角スペースは残す）
    return text.replace("\t", "").replace(" ", "")
