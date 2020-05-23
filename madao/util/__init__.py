from nonebot import logger
import os
import json
import time

# 查询cd记录
interval_dict = {}


def load_config(filename):
    try:
        with open(filename, encoding='utf8') as f:
            config = json.load(f)
            return config
    except Exception as e:
        logger.exception(e)
        return {}


def check_interval(user_id, module, inteval):
    key = str(user_id) + module
    if key not in interval_dict or int(time.time()) - interval_dict[key] >= inteval:
        return True
    else:
        return False


def set_interval(user_id, module):
    key = str(user_id) + module
    interval_dict[key] = int(time.time())
