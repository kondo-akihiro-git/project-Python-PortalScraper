from requests.auth import HTTPBasicAuth

def login(session, base_url, login_id, login_pass, basic_id, basic_pass, logger):
    logger.info("ログイン処理を実行")

    login_payload = {
        "login_id": login_id,
        "login_pass": login_pass,
        "accept": "1",
    }

    response = session.post(
        base_url,
        data=login_payload,
        auth=HTTPBasicAuth(basic_id, basic_pass)
    )

    response.raise_for_status()
    return response
