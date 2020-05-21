from nonebot import logger
import os
import json


def load_config(filename):
    try:
        with open(filename, encoding='utf8') as f:
            config = json.load(f)
            return config
    except Exception as e:
        logger.exception(e)
        return {}
