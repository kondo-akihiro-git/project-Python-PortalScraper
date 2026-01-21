# app/fetch_page.py
from requests.auth import HTTPBasicAuth
import os
from datetime import datetime
from bs4 import BeautifulSoup

def format_text(text: str) -> str:
    # タブと半角スペースのみ削除（全角スペースは残す）
    return text.replace("\t", "").replace(" ", "")

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
    save_weekly_txt(html)
    save_learning_txt(html) 
    save_comment_txt(html) 

# HTMLページ取得
def fetch_html(session, url, bid, bpw):
    res = session.get(url, auth=HTTPBasicAuth(bid, bpw))
    res.raise_for_status()
    return res.text

# 「作業内容」をファイル保存
def save_weekly_txt(html):
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


# 「直近で学んだこと、覚えたこと」をファイル保存
def save_learning_txt(html):
    soup = BeautifulSoup(html, "html.parser")

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(base, "files")
    os.makedirs(out, exist_ok=True)

    ts = datetime.now().strftime("%m%d_%H%M%S")
    path = os.path.join(out, f"learning_{ts}.txt")

    target_div = None

    # 「直近で学んだこと、覚えたこと」を含むdivを探す
    for div in soup.find_all("div"):
        if div.get_text(strip=True).startswith("直近で学んだこと"):
            target_div = div
            break

    if not target_div:
        return path

    content = target_div.find("div", class_="readonly_area")
    if not content:
        return path

    raw = content.get_text(separator="")
    txt = format_text(raw)

    with open(path, "w", encoding="utf-8") as f:
        f.write("■直近で学んだこと、覚えたこと\n")
        f.write(txt)

    return path


# 「コメント欄」をファイル保存
def save_comment_txt(html):
    soup = BeautifulSoup(html, "html.parser")

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(base, "files")
    os.makedirs(out, exist_ok=True)

    ts = datetime.now().strftime("%m%d_%H%M%S")
    path = os.path.join(out, f"comment_{ts}.txt")

    target_div = None

    # 「コメント欄」を含むdivを探す
    for div in soup.find_all("div"):
        text = div.get_text(strip=True)
        if text.startswith("コメント欄"):
            target_div = div
            break

    if not target_div:
        return path

    content = target_div.find("div", class_="readonly_area")
    if not content:
        return path

    raw = content.get_text(separator="")
    txt = format_text(raw)

    with open(path, "w", encoding="utf-8") as f:
        f.write("■コメント欄\n")
        f.write(txt)

    return path
