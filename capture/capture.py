import datetime
import os
import sys
import json
import time

from datetime import datetime
from urllib.parse import parse_qs

import blackboxprotobuf
from mitmproxy import http
from mitmproxy.tools.main import mitmdump


# 通过full_url提取其中的params
def pull_url2params_dict(url: str) -> tuple:
    if url.find("?") == -1: return url, None
    url, params_str = url.split("?")
    ps = params_str.split("&")
    params = dict()
    for p in ps:
        params[p.split("=")[0]] = p.split("=")[1]
    return url, params


# 清空requests_and_responses文件夹
def clear_jsons():
    for root, dirs, files in os.walk("../capture/requests_and_responses"):
        for file in files:
            if file.endswith(".json"):
                os.remove(os.path.join(root, file))


# 将带byte值的字典变成常规字典
def decode_bytes(obj):
    if isinstance(obj, bytes):
        try:
            return obj.decode("utf-8")
        except UnicodeDecodeError:
            return obj.hex()
    elif isinstance(obj, dict):
        return {
            k: decode_bytes(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [
            decode_bytes(i)
            for i in obj
        ]
    return obj


# proto数据流变成dict和dict_type
def proto_bin2dict(bin_content: bin) -> list:
    # struct = protobuf_to_dict(bin_content)
    struct, struct_type = blackboxprotobuf.decode_message(bin_content)
    struct = decode_bytes(struct)
    return struct, struct_type


# 解析出request或response的body部分
def parse_body(flow_part):
    if not flow_part.content:
        return None
    content_type = flow_part.headers.get(
        "content-type",
        ""
    ).lower()
    body = flow_part.content
    # json数据
    if "application/json" in content_type:
        try:
            return json.loads(body.decode("utf-8"))
        except:
            pass
    # 表单数据
    if "application/x-www-form-urlencoded" in content_type:
        try:
            text = body.decode("utf-8")
            return parse_qs(text)
        except:
            pass
    # 普通文本
    if (
            "text/" in content_type
            or "javascript" in content_type
            or "html" in content_type
    ):
        try:
            return body.decode("utf-8")
        except:
            pass
    # proto数据
    if "proto" in content_type:
        d, dt = proto_bin2dict(body)
        d["type"] = dt
        return d
    try:
        text = body.decode("utf-8").strip()

        if text.startswith("{") or text.startswith("["):
            return json.loads(text)
    except:
        pass
    # 二进制用hex存
    return body.hex()


def request(flow: http.HTTPFlow):
    print(flow.request.url)


def response(flow: http.HTTPFlow):
    if flow.request.method == "OPTIONS": return
    url, params = pull_url2params_dict(flow.request.url)
    url_segments = url.split("/")
    while True:
        last_url_segment = url_segments.pop()
        if last_url_segment:
            path = last_url_segment
            break
    if path.find('.') != -1: return
    path = f"../capture/requests_and_responses/{datetime.now().strftime('%H%M%S%f')}_{flow.request.method}_{path}.json"

    # 保存请求+响应
    data = {
        "time": time.time(),
        "request": {
            "method": flow.request.method,
            "url": flow.request.url,
            "headers": dict(flow.request.headers),
            "params": params,
            "body": parse_body(flow.request)
        },
        "response": {
            "status_code": flow.response.status_code,
            "headers": dict(flow.response.headers),
            "body": parse_body(flow.response)
        }
    }
    with open(path, "w+", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)



# 启动代理
# 在localhost:8080
def start_capture():
    clear_jsons()
    sys.argv = [
        "mitmdump",
        "-p",
        "8080",
        "-s",
        "../capture/capture.py"
    ]
    mitmdump()


if __name__ == "__main__":
    start_capture()
