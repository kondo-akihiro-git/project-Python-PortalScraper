from requests.auth import HTTPBasicAuth

def fetch_top_page(session, base_url, basic_id, basic_pass, logger):
    logger.info("/top ページを取得")

    response = session.get(
        f"{base_url}/top",
        auth=HTTPBasicAuth(basic_id, basic_pass)
    )

    response.raise_for_status()
    return response
