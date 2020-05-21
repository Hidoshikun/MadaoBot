from nonebot import on_command, CommandSession
from madao import aiorequests


@on_command('chp', aliases=('彩虹屁',), only_to_me=False)
async def chp(session: CommandSession):
    chp_result = await get_chp()
    # 向用户发送天气预报
    await session.send(chp_result)


async def get_chp() -> str:
    try:
        url = "https://chp.shadiao.app/api.php"
        r = await aiorequests.get(url=url, timeout=5)
        msg = r.text
    except Exception as e:
        msg = "Error: {}".format(type(e))
    return msg
