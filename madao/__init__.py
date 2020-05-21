import nonebot
from os import path


def init(config) -> nonebot.NoneBot:
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'madao.plugins'
    )
    bot = nonebot.get_bot()
    return bot
