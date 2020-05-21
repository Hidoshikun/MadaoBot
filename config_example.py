from nonebot.default_config import *

import os

SUPERUSERS = []

COMMAND_START = {'', '/', '／'}

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), 'madao', 'res')
CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'madao', 'config')

DEFAULT_VALIDATION_FAILURE_EXPRESSION = '你发送的内容格式不太对呢，请检查一下再发送哦～'

MASTER = []  # 从高到低排序

HOST = '127.0.0.1'
PORT = 8080

TENCENT_CHAT_APPID = ''
TENCENT_CHAT_KEY = ''

JJC_KEY = ""
