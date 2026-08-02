import json
import os

from utils import show_dict


# from protobuf_to_dict import protobuf_to_dict, dict_to_protobuf

# 请求或响应 内容包含
def find_content_include(include: str) -> list:
    fs = list()
    for root, dirs, files in os.walk("../capture/requests_and_responses"):
        for file in files:
            with open(f"../capture/requests_and_responses/{file}", "r+", encoding="utf-8") as f:
                # data = json.load(f)
                content = f.read()
                if include in content:
                    print(file)
                    fs.append(file)
    return fs


# 请求或响应 名称包含
def find_file_name_include(include: str) -> list:
    fs = list()
    for root, dirs, files in os.walk("../capture/requests_and_responses"):
        for file in files:
            if include in file:
                print(file)
                fs.append(file)
    return fs


# 响应 内容包含
def find_response_content_include(include: str) -> list:
    fs = list()
    for root, dirs, files in os.walk("../capture/requests_and_responses"):
        for file in files:
            with open(os.path.join(root, file), "r+", encoding="utf-8") as f:
                content = f.read()
                if include in content.split("\"response\"")[1]:
                    print(file)
                    fs.append(file)
    return fs


# 请求 内容包含
def find_request_content_include(include: str) -> list:
    fs = list()
    for root, dirs, files in os.walk("../capture/requests_and_responses"):
        for file in files:
            with open(os.path.join(root, file), "r+", encoding="utf-8") as f:
                content = f.read()
                if include in content.split("\"response\"")[0]:
                    print(file)
                    fs.append(file)
    return fs


# 打开保存的 请求或响应 文件
def open_json(json_file: str) -> dict:
    with open(f"../capture/requests_and_responses/{json_file}", "r", encoding="utf-8") as f:
        return json.load(f)


def do_find_1():
    fs = find_file_name_include("self")
    d = open_json(fs[0])
    show_dict(d)
    pass


def do_find_2():
    fs = find_response_content_include("ABCDEFG")
    d = open_json(fs[0])
    show_dict(d)
    pass


if __name__ == '__main__':
    # do_find_1()
    do_find_2()
    pass
