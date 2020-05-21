from nonebot import CommandSession, on_command
from madao import aiorequests
from nonebot import logger
import json


@on_command("nuannuan", aliases=("暖暖", "本周暖暖"), only_to_me=False)
async def nuannuan(session: CommandSession):
    url = "http://nuannuan.yorushika.co:5000/"
    r = await aiorequests.get(url=url, timeout=5)
    data = await r.json()
    logger.debug(data)
    if data["success"]:
        msg = data.get("content", "default content")
        msg += "\nPowered by 露儿[Yorushika]"
    else:
        msg = "Error"

    await session.send(msg)
