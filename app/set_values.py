# app/set_values.py
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup


# ===== テストデータ定義 =====
TEST_WORKING_MEMOS = [
    "【テスト】作業内容1",
    "【テスト】作業内容2",
    "【テスト】作業内容3",
    "【テスト】作業内容4",
    "【テスト】作業内容5",
    "【テスト】作業内容6",
    "【テスト】作業内容7",
]

TEST_LEARNING = "【テスト】直近で学んだこと"
TEST_COMMENT = "【テスト】コメント欄"


def set_values(session, url, basic_id, basic_pass, logger):
    html = fetch_html(session, url, basic_id, basic_pass)
    set_value(session, url, basic_id, basic_pass, html, logger)


def fetch_html(session, url, bid, bpw):
    res = session.get(url, auth=HTTPBasicAuth(bid, bpw))
    res.raise_for_status()
    return res.text


def set_value(session, url, basic_id, basic_pass, html, logger):
    soup = BeautifulSoup(html, "html.parser")

    form = soup.find("form", id="weekly_report")
    if not form:
        raise RuntimeError("weekly_report form not found")

    payload = {}

    # hidden input（必須）
    for inp in form.find_all("input", type="hidden"):
        payload[inp["name"]] = inp.get("value", "")

    # ===== 作業内容（7日分・固定テストデータ）=====
    table = soup.find("table", id="weekly_report_list")
    if table:
        rows = table.find("tbody").find_all("tr")

        for idx, tr in enumerate(rows):
            if idx >= len(TEST_WORKING_MEMOS):
                break

            textarea = tr.find("textarea", attrs={"name": True})
            if not textarea:
                continue

            name = textarea["name"]

            # working_memo のみ対象
            if name.endswith("[working_memo]"):
                payload[name] = TEST_WORKING_MEMOS[idx]

    # ===== 直近で学んだこと =====
    if form.find("textarea", attrs={"name": "studying_memo"}):
        payload["studying_memo"] = TEST_LEARNING

    # ===== コメント欄 =====
    if form.find("textarea", attrs={"name": "comment"}):
        payload["comment"] = TEST_COMMENT

    # 保存
    payload["save"] = "1"

    logger.info("週報（作業内容7日分・学習・コメント）をテストデータで保存")

    res = session.post(
        url,
        data=payload,
        auth=HTTPBasicAuth(basic_id, basic_pass),
    )
    res.raise_for_status()

    logger.info("保存完了")
