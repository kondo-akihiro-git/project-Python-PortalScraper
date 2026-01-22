# app/set_values.py
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup


def set_values(session, url, basic_id, basic_pass, logger, data):
    url = build_url(url)
    html = fetch_html(session, url, basic_id, basic_pass)
    set_value(session, url, basic_id, basic_pass, html, logger, data)


def fetch_html(session, url, bid, bpw):
    res = session.get(url, auth=HTTPBasicAuth(bid, bpw))
    res.raise_for_status()
    return res.text


def set_value(session, url, basic_id, basic_pass, html, logger, data):
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
            if idx >= len(data["weekly"]):
                break

            textarea = tr.find("textarea", attrs={"name": True})
            if not textarea:
                continue

            name = textarea["name"]

            # working_memo のみ対象
            if name.endswith("[working_memo]"):
                payload[name] = data["weekly"][idx]["content"]

    # ===== 直近で学んだこと =====
    if form.find("textarea", attrs={"name": "studying_memo"}):
        payload["studying_memo"] = data.get("learning", "")

    # ===== コメント欄 =====
    if form.find("textarea", attrs={"name": "comment"}):
        payload["comment"] = data.get("comment", "")

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


def build_url(base_url: str) -> str:
    """
    get_weekから取得した週情報を使ってURLを作成
    """
    return (
        f"{base_url}/weekly_report"
    )