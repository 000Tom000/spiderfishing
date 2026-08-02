from . import common


def show_dict(d: dict) -> None:
    for k, v in d.items():
        print(f"{k} : {v}")

def get_cookie_by_name(name: str) -> dict:
    cookies = common.get_cookies()
    for cookie in cookies:
        if cookie['name'] == name:
            return cookie
