import json #用于处理json数据
import urllib.parse # 用于对URL进行解析和构建
 
import requests #用于发送HTTTP请求
 
corpid = ''  # 企业ID
agentid =   # 应用ID
corpsecret = ''  # 应用Secret
touser = ''  # 接收消息的用户
 
# 企业微信API的基础URL
base = 'https://qyapi.weixin.qq.com'
 
# 请求登录凭证（access-token）
 
# 构造函数(获取access-token的API URL)
access_token_api = urllib.parse.urljoin(base, '/cgi-bin/gettoken') # 使用urllib.parse.urljoin来构建获取access-token的完整url
# 定义请求参数（包括企业ID，应用密钥）
params = {'corpid': corpid, 'corpsecret': corpsecret}
# 发送GET请求获取access-token，并且将json响应转化为python字典
response = requests.get(url=access_token_api, params=params).json()
# 从响应中获取access-token
access_token = response['access_token']
 
# 发送消息
# 构建发送消息的完整URL，包含access-token
message_send_api = urllib.parse.urljoin(base, f'/cgi-bin/message/send?access_token={access_token}')
# 定义要发送的消息数据（文本格式）
data = {'touser': touser, 'msgtype': 'text', 'agentid': agentid, 'text': {'content': '测试数据：hello world!'}}
# 发送POST请求以发送消息， 并将json响应转化为python字典
response = requests.post(url=message_send_api, data=json.dumps(data)).json()
 
# 当请求返回值为0时(异常处理)
if response['errcode'] == 0:
    print('发送成功')
else:
    print(response)

