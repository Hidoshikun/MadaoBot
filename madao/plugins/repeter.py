import random
from nonebot import get_bot, CQHttpError
from nonebot import logger

bot = get_bot()

PROB_A = 0.5
group_stat = {}  # group_id: (last_msg, repeat_cnt)


@bot.on_message('group')
async def random_repeater(context):
    group_id = context['group_id']
    msg = str(context['message'])

    if group_id not in group_stat:
        group_stat[group_id] = (msg, 1)
        return

    last_msg, repeat_cnt = group_stat[group_id]
    if last_msg == msg:
        repeat_cnt += 1
        if repeat_cnt >= 3:
            try:
                if random.random() < PROB_A:
                    group_stat[group_id] = (msg, 0)
                    await bot.send(context, msg)
            except CQHttpError as e:
                logger.error(f'复读失败: {type(e)}')
        else:
            group_stat[group_id] = (msg, repeat_cnt)
    else:
        group_stat[group_id] = (msg, repeat_cnt)
