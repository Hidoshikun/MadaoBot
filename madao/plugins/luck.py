from nonebot import on_command, CommandSession
import nonebot
import os
import datetime
import hashlib
from os import path

bot = nonebot.get_bot()
res_root = os.path.join(bot.config.RESOURCE_DIR, 'luck_img')


@on_command('luck', aliases=('抽签',), only_to_me=False)
async def luck(session: CommandSession):
    user_id = session.event.user_id
    luck_result = get_luck(user_id)
    await session.send(luck_result)


def get_luck(user_id) -> str:
    random_num = get_page_num(user_id)
    img_path = res_root + '/luck_' + str(random_num) + '-min.jpg'
    msg = "[CQ:at,qq=%s]" % user_id + "[CQ:image,file=file:///{}]\n".format(img_path)
    msg = msg.strip()
    return msg


def get_page_num(user_id) -> int:
    today = datetime.date.today()
    formatted_today = int(today.strftime('%y%m%d'))
    str_num = str(formatted_today * user_id)
    md5 = hashlib.md5()
    md5.update(str_num.encode('utf-8'))
    res = md5.hexdigest()
    return int(res.upper(), 16) % 100 + 1
