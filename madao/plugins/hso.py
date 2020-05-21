from nonebot import on_command, CommandSession
from madao import aiorequests
import random

# 查询cd记录
interval_dict = {}


def check_interval(user_id):
    if user_id not in interval_dict or int(time.time()) - interval_dict[user_id] >= 120:
        return True
    else:
        return False


def set_interval(user_id):
    interval_dict[user_id] = int(time.time())


@on_command('hso', aliases=('色图',), only_to_me=False)
async def hso(session: CommandSession):
    user_id = session.ctx['user_id']
    if not check_interval(user_id):
        session.finish('您色的太快了！请让Madao休息一下，过几分钟后再来色吧', at_sender=True)

    image = await get_hso()

    set_interval(user_id)
    await session.send(image)


async def get_hso():
    page = random.randint(1, 50)
    params = "limit=20&page={}".format(page)
    api_url = "https://konachan.com/post.json?{}".format(params)
    r = await aiorequests.get(api_url, timeout=(5, 60))
    img_json = await r.json()

    tmp_list = []
    for item in img_json:
        if item["rating"] == "s":
            tmp_list.append(item)
    img_json = tmp_list

    if len(img_json) == 0:
        msg = "未能找到所需图片"
    else:
        idx = random.randint(0, len(img_json) - 1)
        img = img_json[idx]
        msg = "[CQ:image,file={},destruct=0]".format(img["sample_url"])

    return msg
