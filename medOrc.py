import requests
import json
import time

# 智诊科技开发文档 图片分析

url = "https://api.wisediag.com/med_ocr"
stream = False


payload = {
    "image_url": [
        "https://pic.wisediag.com/zchat/file/70eaca4e-9825-451d-b6b2-82907f4dcf2b.png",
    ],
    "query": "请分析以上报告",
    "stream": stream,
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-/BP7Ouh4WX9zxNIciwaF0XBgIrdEqSa0jUVBUQSxSX0=",
}

try:
    response = requests.post(url, json=payload, headers=headers, stream=stream)
    response.raise_for_status()
except requests.HTTPError as http_err:
    try:
        error_data = response.json()
        print("请求错误:", error_data)
    except Exception as parse_err:
        print("请求错误:", http_err)
    exit(1)
except requests.RequestException as e:
    print("请求错误:", e)
    exit(1)


if stream:
    print("开始接收流式数据：")
    res = ""
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            if decoded_line.startswith("data: "):
                data_str = decoded_line[len("data: ") :]
                try:
                    data = json.loads(data_str)
                    print(data.get("response", ""), end="")
                    res += data.get("response", "")
                except json.JSONDecodeError as e:
                    print("JSON 解析错误：", e)
    data["response"] = res
    result = data
else:
    result = response.json()

print()


while True:
    print("程序运行中...")
    print("结果:", json.dumps(result, ensure_ascii=False, indent=2))
    time.sleep(10)  # 每10秒执行一次
