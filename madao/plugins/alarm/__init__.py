from nonebot import scheduler
import nonebot
from madao import util
from datetime import datetime
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
import os
from nonebot import logger

push_group = [917126871, 953877394, 863436362]
# push_group = [917126871]

# 再此指定舰娘
kanmusu = "hagikaze"

bot = nonebot.get_bot()
res_root = os.path.join(bot.config.RESOURCE_DIR, 'alarm', kanmusu)
cfg_root = os.path.join(bot.config.CONFIG_DIR, 'alarm.json')
config = util.load_config(cfg_root)[kanmusu]


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
        except CQHttpError:
            pass
