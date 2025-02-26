from PyOfficeRobot.core.WeChatType import WeChat
import time
import requests
import re
import traceback
import logging
import pyperclip
from pywinauto import keyboard
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            f'wechat_bot_{datetime.now().strftime("%Y%m%d")}.log', encoding="utf-8"
        ),
        logging.StreamHandler(),
    ],
)


class WeChatBot:
    def __init__(self):
        # 初始化重试配置
        self.retry_count = 3
        self.retry_interval = 5

        # 初始化微信
        self.initialize_wechat()

        # 基础配置
        self.bot_name = "测试AI机器人"  # 机器人名称
        # self.target = "AI研究小分队"  # 目标群名
        self.target = "墨七"  # 目标群名
        self.use_dify = True  # 是否使用 Dify API

        self.dify_api_key = ""
        self.dify_api_url = ""

    def initialize_wechat(self):
        """初始化微信，包含重试机制"""
        for attempt in range(self.retry_count):
            try:
                self.wx = WeChat()
                logging.info("微信初始化成功")
                return
            except Exception as e:
                logging.error(
                    f"微信初始化失败 (尝试 {attempt + 1}/{self.retry_count}): {str(e)}"
                )
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_interval)
                else:
                    raise Exception("微信初始化失败，已达到最大重试次数")

    def call_dify_api(self, prompt):
        """调用Dify API，包含重试机制"""
        headers = {
            "Authorization": f"Bearer {self.dify_api_key}",
            "Content-Type": "application/json",
        }

        print("问题内容111", prompt)
        data = {
            "inputs": {},
            "query": prompt,
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "abc-123",
        }
        for attempt in range(self.retry_count):
            try:
                response = requests.post(
                    self.dify_api_url, headers=headers, json=data, timeout=100
                )
                if response.status_code == 200:
                    return response.json()["answer"]
            except Exception as e:
                logging.error(
                    f"API调用出错 (尝试 {attempt + 1}/{self.retry_count}): {str(e)}"
                )
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_interval)
        return "抱歉，当前系统繁忙，请稍后再试。"

    def get_last_message(self):
        """获取最新消息，包含重试机制"""
        for attempt in range(self.retry_count):
            try:
                return self.wx.GetLastMessage
            except Exception as e:
                logging.error(
                    f"获取消息失败 (尝试 {attempt + 1}/{self.retry_count}): {str(e)}"
                )
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_interval)
        return None

    def format_response(self, user, question, content):
        """格式化回复消息"""
        logging.info(f"用户: {user}\n问题: {question}\n回复: {content}")
        return f"回复【{user}】问题:\n{question}\n---------------\n{content}"

    def is_mentioned(self, message):
        """检查是否被@"""
        return f"@{self.bot_name}" in str(message)

    def extract_question(self, message):
        """提取@之后的问题内容"""
        message = str(message)
        pattern = f"@{self.bot_name}(.*)"
        match = re.search(pattern, message)
        if match:
            return match.group(1).strip()
        return ""

    def parse_message(self, msg_info):
        """解析消息内容"""
        try:
            if isinstance(msg_info, tuple) and len(msg_info) >= 2:
                name = msg_info[0]
                content = msg_info[1]
                logging.info(f"name: {name}, 内容: {content}")
                return {"name": name, "content": content}
            return None
        except Exception as e:
            logging.error(f"解析消息失败: {str(e)}")
            return None

    def send_message(self, name, message):
        """发送消息到指定窗口"""
        try:
            logging.info(f"正在发送消息到 {name}: {message}")
            self.wx.ChatWith(name)
            time.sleep(0.3)
            pyperclip.copy(message)
            keyboard.send_keys("^v")
            time.sleep(0.1)
            keyboard.send_keys("{ENTER}")
            time.sleep(0.1)
            logging.info("消息发送成功")
            return True
        except Exception as e:
            logging.error(f"发送消息失败: {str(e)}")
            return False

    def monitor_messages(self):
        """监听微信消息"""
        logging.info(f"开始监听微信消息...\n机器人名称: {self.bot_name}")
        last_message = None

        while True:
            try:
                msg_info = self.get_last_message()
                if msg_info and msg_info != last_message:
                    logging.info(f"收到新消息: {msg_info}")
                    last_message = msg_info
                    msg_data = self.parse_message(msg_info)
                    if not msg_data:
                        continue
                    content = msg_data.get("content", "")
                    if self.is_mentioned(content):
                        question = self.extract_question(content)
                        if question:
                            response = self.call_dify_api(question)
                            formatted_response = self.format_response(
                                msg_data.get("name"), question, response
                            )
                            self.send_message(self.target, formatted_response)
                time.sleep(1)
            except Exception as e:
                logging.error(f"监听消息时出错: {str(e)}")
                time.sleep(self.retry_interval)

    def run(self):
        """运行机器人"""
        try:
            self.monitor_messages()
        except KeyboardInterrupt:
            logging.info("程序已手动停止")
        except Exception as e:
            logging.error(f"程序运行出错: {str(e)}")
            traceback.print_exc()


if __name__ == "__main__":
    bot = WeChatBot()
    bot.run()
