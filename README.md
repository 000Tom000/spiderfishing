# 🕷️ Spider

> 基于 mitmproxy 的 HTTPS 流量捕获工具 —— 配合 Selenium 浏览器自动化，拦截并分析 Web 应用的 API 通信。

**Spider** 通过中间人代理（MITM）的方式，将浏览器发出的 HTTP/HTTPS 请求和响应拦截下来，自动解析多种格式的 body（JSON / 表单 / 文本 / Protobuf），并保存为结构化 JSON 文件，方便后续查找与分析。

---

## ✨ 实际功能

- 🔍 **HTTPS 抓包** —— 基于 mitmproxy 在 `localhost:8080` 启动代理，拦截所有经过的请求和响应
- 🌐 **浏览器自动化** —— 通过 Selenium + ChromeDriver 启动配置了代理的 Chrome 浏览器，无需手动设置系统代理
- 📦 **多格式 Body 解析** —— 自动识别并解析：
  - JSON（`application/json`）
  - 表单（`application/x-www-form-urlencoded`）
  - 纯文本 / JavaScript / HTML
  - **Protobuf**（通过 blackboxprotobuf 解码为可读字典）
  - 二进制数据（fallback 为 hex 字符串）
- 💾 **结构化存储** —— 每个请求+响应对保存为一个独立 JSON 文件，包含 URL、Method、Headers、Params、Body、Status Code、时间戳
- 🔎 **查找工具** —— 按文件名、请求内容、响应内容在已捕获的数据中快速检索
- 🍪 **Cookies 持久化** —— 支持从 Chrome 导出 cookies 到本地 JSON 文件，下次启动时加载，避免重复登录
- 🎯 **以抖音为例** —— 当前代码以 `douyin.com` 作为目标站点，可改为任意网站

---

## 📦 环境依赖

```bash
pip install -r requirements.txt
```

| 依赖 | 用途 |
| :--- | :--- |
| `mitmproxy` | 中间人代理核心，拦截 HTTP/HTTPS 流量 |
| `selenium` | 启动和控制 Chrome 浏览器，自动配置代理 |
| `blackboxprotobuf` | 解码 Protobuf 格式的请求/响应 body |

此外需要 **ChromeDriver**（已包含在 `chromedriver/` 目录中，版本需与本机 Chrome 匹配）。

---

## 🚀 使用方式

### 1. 启动抓包代理 + 浏览器

```bash
cd opening
python opening.py
```

这将会：
1. 清空上次的抓包记录
2. 在 `localhost:8080` 启动 mitmproxy 代理
3. 打开配置了该代理的 Chrome 浏览器，访问抖音
4. 加载本地 cookies（如已保存）
5. 所有经过代理的 API 请求和响应自动保存到 `capture/requests_and_responses/`

### 2. 首次登录（获取 cookies）

```bash
cd opening
# 编辑 opening.py，将最后一行的 opening() 改为 login()
python opening.py
```

在打开的浏览器中手动完成登录，然后在终端按回车保存 cookies 到 `data/cookies.json`。

### 3. 查找已捕获的数据

```bash
cd capture
python finding.py
```

或在代码中调用：

```python
from capture.finding import find_content_include, find_file_name_include, open_json

# 按文件名模糊搜索
files = find_file_name_include("search_keyword")

# 按响应内容搜索
files = find_response_content_include("some_text")

# 打开指定文件
data = open_json(files[0])
print(data)
```

---

## 🧩 项目结构

```
spider/
├── capture/
│   ├── capture.py              # mitmproxy 代理脚本，拦截请求/响应并保存为 JSON
│   ├── finding.py              # 已捕获数据的检索工具
│   └── requests_and_responses/ # 抓包输出目录（JSON 文件）
├── opening/
│   └── opening.py              # Selenium 浏览器启动 + cookies 管理 + 代理联动
├── chromedriver/
│   ├── chromedriver.exe        # ChromeDriver（需与本地 Chrome 版本匹配）
│   └── readme.txt
├── utils/
│   ├── common.py               # cookies 读取
│   ├── build.py                # headers / params 构建辅助
│   └── index.py                # dict 打印、按名称取 cookie
├── data/
│   └── cookies.json            # 持久化保存的浏览器 cookies
├── requirements.txt
└── README.md
```

---

## ⚠️ 注意事项

- **HTTPS 证书**：mitmproxy 拦截 HTTPS 需要安装其根证书，否则浏览器会报安全警告。首次使用前需在系统中信任 mitmproxy 的 CA 证书。
- **ChromeDriver 版本**：`chromedriver/` 中的 exe 需与本机安装的 Chrome 浏览器主版本一致（当前为 150 大版本）。版本不匹配会导致 Selenium 无法启动浏览器。
- **ChromeDriver 版本资源**：https://googlechromelabs.github.io/chrome-for-testing/
- **这不是网络爬虫**：本项目捕获的是浏览器发出的 API 请求/响应，不是解析网页 HTML。
- **路径约定**：代码中使用 `../capture/`、`../data/` 等相对路径，需在对应子目录（`capture/`、`opening/`）下运行脚本，否则路径会出错。

---

## 📄 开源协议

MIT © 000Tom000
