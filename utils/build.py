def build_headers():
    headers = dict()
    headers["user-agent"] = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
    )
    headers["accept"] = "application/json"
    headers["content-type"] = "application/json;charset=utf-8"
    return headers


def build_params():
    params = dict()
    params["id"] = 3
    return params
