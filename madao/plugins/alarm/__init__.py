from nonebot import scheduler
import nonebot
from madao import util
from datetime import datetime
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
import os
from nonebot import logger

# 还8能通过命令管理推送的群
push_group = [953877394, 863436362]
# push_group = [917126871]

# 再此指定舰娘
kanmusu = "hagikaze"

bot = nonebot.get_bot()
res_root = os.path.join(bot.config.RESOURCE_DIR, 'alarm', kanmusu)
res2_root = os.path.join(bot.config.RESOURCE_DIR, 'others')
cfg_root = os.path.join(bot.config.CONFIG_DIR, 'alarm.json')
config = util.load_config(cfg_root)[kanmusu]


# 舰娘报时
@scheduler.scheduled_job('cron', hour='*')
# @scheduler.scheduled_job('interval', minutes=1)
async def _():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour < 10:
        key = "0" + str(now.hour) + "00"
    else:
        key = str(now.hour) + "00"

    text_msg = config[key] + "\n"
    record = config["prefix"] + key + ".mp3"
    record_msg = f'[CQ:record,file=file:///{res_root}\\{record}]'
    for group in push_group:
        try:
            await bot.send_group_msg(group_id=group, message=text_msg)
            await bot.send_group_msg(group_id=group, message=record_msg)
        except CQHttpError as e:
            logger.error(f'CQHttpError: {e}')


# 经验药提醒小助手
@scheduler.scheduled_job('cron', hour='*')
# @scheduler.scheduled_job('interval', minutes=1)
async def _():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour % 6 == 0:
        reminder = f'[CQ:image,file=file:///{res2_root}\\exp_remind.png]\n'
        for group in push_group:
            try:
                await bot.send_group_msg(group_id=group, message=reminder)
            except CQHttpError as e:
                logger.error(f'CQHttpError: {e}')
    else:
        pass
