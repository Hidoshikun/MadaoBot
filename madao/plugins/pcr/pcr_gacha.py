# -*- coding:utf-8 -*-
from nonebot import on_command, CommandSession
import nonebot
from madao import util
import random
from PIL import Image
import os
from nonebot import logger
import math
import time

# 国服only

bot = nonebot.get_bot()
res_root = os.path.join(bot.config.RESOURCE_DIR, 'pcr')
cfg_root = os.path.join(bot.config.CONFIG_DIR, 'pcr.json')
config = util.load_config(cfg_root)

# 选池子
pool = config["BL_pool"]
# 取概率
up_prob = pool["up_prob"]
s3_prob = pool["s3_prob"]
s2_prob = pool["s2_prob"]
# 取卡池
up = pool["up"]
star3 = pool["star3"]
star2 = pool["star2"]
star1 = pool["star1"]

# 查询cd记录
interval_dict = {}


def check_interval(user_id):
    if user_id not in interval_dict or int(time.time()) - interval_dict[user_id] >= 120:
        return True
    else:
        return False


def set_interval(user_id):
    interval_dict[user_id] = int(time.time())


@on_command('gacha', aliases=('来发十连',), only_to_me=False)
async def gacha(session: CommandSession):
    await session.send("pcr请输入 /pcr十连，fgo请输入 /fgo十连")


# gacha
@on_command('pcr_gacha', aliases=('pcr十连',), only_to_me=False)
async def pcr_gacha(session: CommandSession):
    user_id = session.ctx['user_id']
    if not check_interval(user_id):
        session.finish('您抽的太快啦，请让Madao休息一下，过几分钟再抽吧~', at_sender=True)

    result = []
    up_num, star3_num, star2_num = 0, 0, 0

    at_msg = ''
    if session.ctx['message_type'] == 'group':
        at_msg = '[CQ:at,qq={}]\n'.format(str(user_id))

    up_str = ""
    for c in up:
        up_str += " " + str(c) + "★★★"
    at_msg += "本期up角色：" + up_str
    at_msg += "\n本次抽卡结果：\n"

    text_result = ""

    for n in range(9):
        i = random.random() * 1000
        if i <= up_prob:
            up_num += 1
            chara = random.choice(up)
            text_result += str(chara) + "★3(up) "
            result.append(chara)
        elif s3_prob >= i > up_prob:  # 3星
            star3_num += 1
            chara = random.choice(star3)
            text_result += str(chara) + "★3 "
            result.append(chara)
        elif s2_prob >= i > s3_prob:  # 2星
            star2_num += 1
            chara = random.choice(star2)
            text_result += str(chara) + "★2 "
            result.append(chara)
        else:  # 1星
            chara = random.choice(star1)
            text_result += str(chara) + "★ "
            result.append(chara)

    if random.random() * 1000 > s3_prob:
        star2_num += 1
        chara = random.choice(star2)
        text_result += str(chara) + "★2 "
        result.append(chara)
    else:
        star3_num += 1
        chara = random.choice(star3)
        text_result += str(chara) + "★3 "
        result.append(chara)

    name = session.ctx['user_id']
    a = 0
    background = Image.new('RGBA', (330, 135), color='lavenderblush')

    for x in range(5):
        for y in range(2):
            pic = Image.open(os.path.join(res_root, result[a] + '.png'))
            background.paste(pic, (x * 65 + 5, y * 65 + 5))
            a += 1
    background.save(res_root + f'\\out\\{name}.png')

    text_result += "\n★3数量{}， ★2数量{}".format(star3_num + up_num, star2_num)

    if up_num >= 1:
        text_result += "，抽到了本期up，大概这就是海豹吧"

    if star3_num + up_num >= 2:
        text_result += "，欧洲狗吃我一刀！"
    elif star3_num == 1:
        text_result += "，有三星就挺好的，你说对不"
    elif star3_num == 0 and up_num == 0 and star2_num == 1:
        text_result += "，19密石get，人生还是如此波澜不惊"
    set_interval(user_id)
    await session.send(at_msg + f'[CQ:image,file=file:///{res_root}\\out\\{name}.png]\n' + text_result)


@on_command('tenjou', aliases=('来一井',), only_to_me=False)
async def tenjou(session: CommandSession):
    user_id = session.ctx['user_id']
    if not check_interval(user_id):
        msg = "您抽的太快啦，请让Madao休息一下，过几分钟再抽吧~"
        await session.send(msg)
        return

    at_msg = ''
    if session.ctx['message_type'] == 'group':
        at_msg = '[CQ:at,qq={}]\n'.format(str(user_id))

    up_str = ""
    for c in up:
        up_str += " " + str(c) + "★3"
    at_msg += "本期up角色：" + up_str
    at_msg += "\n本次抽卡结果："

    up_num, star1_num, star2_num, star3_num, result, first_up = gacha10(0, 0, 0, 0, 0, [], 0)

    text_result = ""

    name = session.ctx['user_id']
    count = 0
    w = 4
    h = math.ceil(len(result) / w)
    background = Image.new('RGBA', (w * 65 + 5, h * 65 + 5), color='lavenderblush')
    for y in range(h):
        for x in range(w):
            if count < len(result):
                pic = Image.open(os.path.join(res_root, result[count] + '.png'))
                background.paste(pic, (x * 65 + 5, y * 65 + 5))
                count += 1

    background.save(res_root + f'\\out\\{name}.png')

    text_result += "\n★3数量{}， ★2数量{}".format(star3_num + up_num, star2_num)

    text_result += "， 女神密石数量{}".format(star3_num * 50 + star2_num * 10 + star1_num)

    if first_up == 0:
        text_result += "， 并没有抽出本期up，恭喜你遇见了12%的概率，还是乖乖去井出来吧"
    elif first_up <= 40:
        text_result += "， 在第{}抽抽出了本期up，你的喜悦我收到了，滚回去喂鲨鱼吧".format(first_up)
    elif first_up <= 100:
        text_result += "， 在第{}抽抽出了本期up，亚洲中上水平，请烧香拜佛再接再厉".format(first_up)
    elif first_up <= 220:
        text_result += "， 在第{}抽抽出了本期up，平均水平，咱就有事没事日行一善攒点人品吧".format(first_up)
    else:
        text_result += "， 在第{}抽抽出了本期up，咱们好歹出货了就不讲究什么了".format(first_up)

    set_interval(user_id)
    await session.send(at_msg + f'[CQ:image,file=file:///{res_root}\\out\\{name}.png]' + text_result)


def gacha10(countdown, up_num, star3_num, star2_num, star1_num, result, first_up):
    for n in range(9):
        i = random.random() * 1000
        if i <= up_prob:
            up_num += 1
            if first_up == 0:
                first_up = int(countdown + i)
            chara = random.choice(up)
            result.append(chara)
        elif s3_prob >= i > up_prob:  # 3星
            star3_num += 1
            chara = random.choice(star3)
            result.append(chara)
        elif s2_prob >= i > s3_prob:  # 2星
            star2_num += 1
        else:  # 1星
            star1_num += 1

    if random.random() * 1000 > s3_prob:
        star2_num += 1
    else:
        star3_num += 1
        chara = random.choice(star3)
        result.append(chara)

    if countdown != 300:
        return gacha10(countdown + 10, up_num, star3_num, star2_num, star1_num, result, first_up)
    else:
        return up_num, star1_num, star2_num, star3_num, result, first_up
