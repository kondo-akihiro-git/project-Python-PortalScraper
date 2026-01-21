# app/set_values.py
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

def set_values(session, url, basic_id, basic_pass, logger):
    html = fetch_html(session, url, basic_id, basic_pass)
    set_weekly_value(session, url, basic_id, basic_pass,html, logger)

# HTMLページ取得
def fetch_html(session, url, bid, bpw):
    res = session.get(url, auth=HTTPBasicAuth(bid, bpw))
    res.raise_for_status()
    return res.text


def set_weekly_value(session, url, basic_id, basic_pass,html, logger):
    soup = BeautifulSoup(html, "html.parser")

    form = soup.find("form", id="weekly_report")
    if not form:
        raise RuntimeError("weekly_report form not found")

    payload = {}

    # hidden input を全部詰める
    for inp in form.find_all("input", type="hidden"):
        payload[inp["name"]] = inp.get("value", "")

    # 作業内容 textarea → 全部 "1"
    for ta in form.find_all("textarea"):
        name = ta.get("name")
        if name and name.startswith("detail["):
            payload[name] = "1"

    # 保存ボタン押下相当
    payload["save"] = "1"

    logger.info("週報 作業内容を '1' で保存します")

    res = session.post(
        url,
        data=payload,
        auth=HTTPBasicAuth(
            basic_id, basic_pass
        ),
    )
    res.raise_for_status()

    logger.info("保存完了")

def set_learning_value(html):
    pass
def set_comment_value(html):
    pass