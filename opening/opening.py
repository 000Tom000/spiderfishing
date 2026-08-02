import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from capture.capture import clear_jsons

# chrome保存cookies
def chrome2cookies(chrome: webdriver.Chrome) -> None:
    with open("../data/cookies.json", "w+", encoding="utf-8") as file:
        json.dump(chrome.get_cookies(), file, ensure_ascii=False, indent=4)


# cookies装载到chrome
def cookies2chrome(chrome: webdriver.Chrome) -> webdriver.Chrome:
    with open("../data/cookies.json", "r+", encoding="utf-8") as file:
        for cookie in json.load(file):
            if cookie["domain"] in chrome.current_url:
                chrome.add_cookie(cookie)
        return chrome


# 登录初始化cookies
def login():
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server=http://127.0.0.1:8080")

    project_path = "\\".join(os.getcwd().split("\\")[:-1])
    project_path = os.path.join(project_path, "chromedriver")
    service = Service(os.path.join(project_path, "chromedriver.exe"))

    chrome = webdriver.Chrome(options=options, service=service)
    chrome.get("https://www.douyin.com")
    chrome.maximize_window()
    print("浏览器已就绪")
    while True:
        input("完成登录按回车保存cookies...")
        chrome2cookies(chrome)


# 可DIY
# 自定义操作
def opening():
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server=http://127.0.0.1:8080")

    project_path = "\\".join(os.getcwd().split("\\")[:-1])
    project_path = os.path.join(project_path, "chromedriver")
    service = Service(os.path.join(project_path, "chromedriver.exe"))

    chrome = webdriver.Chrome(options=options, service=service)
    chrome.get("https://www.douyin.com")
    chrome = cookies2chrome(chrome)
    chrome.refresh()
    chrome.maximize_window()
    print("浏览器已就绪")
    while True:
        input("完成操作按回车保存cookies...")
        chrome2cookies(chrome)


if __name__ == '__main__':
    # 登录cookies
    # login()
    # 操作抓包
    opening()
    pass
