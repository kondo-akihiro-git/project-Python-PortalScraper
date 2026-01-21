from requests.auth import HTTPBasicAuth

def access_with_basic_auth(session, base_url, basic_id, basic_pass, logger):
    logger.info("BASIC認証付きでトップページにアクセス")
    response = session.get(
        base_url,
        auth=HTTPBasicAuth(basic_id, basic_pass)
    )
    response.raise_for_status()
    return response
