from nonebot import on_command, CommandSession
from os import path

import random
from nonebot import get_bot
from nonebot import logger

bot = get_bot()

PROB_A = 0.5
group_stat = {}  # group_id: (last_msg, repeat_cnt)


@bot.on_message('group')
async def random_repeater(context):
    msg = str(context['message'])
    logger.debug(msg)
    if "晚安" in msg:
        random_num = 1000 + random.randint(1, 126)

        img_path = path.join(path.dirname(path.dirname(__file__)), 'res', 'meat', str(random_num) + '.gif')

        msg = "[CQ:image,file=file:///{}]\n".format(img_path)
        msg = msg.strip()
        await bot.send(context, msg)
