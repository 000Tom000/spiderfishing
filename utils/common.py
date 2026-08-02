import json


def get_cookies() -> list:
    with open('../data/cookies.json', 'r', encoding='utf-8') as file:
        return json.load(file)

