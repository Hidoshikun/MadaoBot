from nonebot import on_command, CommandSession
from os import path
import random


@on_command('goodnight', aliases=('晚安',), only_to_me=False)
async def luck(session: CommandSession):
    random_num = 1000 + random.randint(1, 126)

    img_path = path.join(path.dirname(path.dirname(__file__)), 'res', 'meat', str(random_num) + '.gif')

    msg = "[CQ:image,file=file:///{}]\n".format(img_path)
    msg = msg.strip()
    await session.send(msg)

