# -*- coding:utf-8 -*-
from nonebot import on_command, CommandSession
import nonebot
import random
from PIL import Image
import os
from nonebot import logger
from madao import util
from typing import List
import math

# 国服only
# 卡池参考20200510国服卡池，卡池名称：复刻 唠唠叨叨帝都圣杯奇谭推荐召唤
# 保底机制参考 https://zhuanlan.zhihu.com/p/75636518
# 每日替换推荐从者太麻烦了，索性先8管，全部加进卡池去
# 太懒了，卡牌数量多且重名卡多，卡池懒得维护了

bot = nonebot.get_bot()
res_root = os.path.join(bot.config.RESOURCE_DIR, 'fgo')
cfg_root = os.path.join(bot.config.CONFIG_DIR, 'fgo.json')
config = util.load_config(cfg_root)

__module__ = "fgo_gacha"

# 选池子
pool = config["BL"]

# 取概率

# 从者
# 限定/推荐
limited_s5_servant_prob = pool["limited_s5_servant_prob"]
limited_s3_servant_prob = pool["limited_s3_servant_prob"]
recommend_s4_servant_prob = pool["recommend_s4_servant_prob"]
recommend_s3_servant_prob = pool["recommend_s3_servant_prob"]
# 普池
s5_servant_prob = pool["s5_servant_prob"] - limited_s5_servant_prob
s4_servant_prob = pool["s4_servant_prob"] - recommend_s4_servant_prob
s3_servant_prob = pool["s3_servant_prob"] - limited_s3_servant_prob - recommend_s3_servant_prob

# 礼装
# 限定/推荐
limited_s5_craft_prob = pool["limited_s5_craft_prob"]
limited_s4_craft_prob = pool["limited_s4_craft_prob"]
limited_s3_craft_prob = pool["limited_s3_craft_prob"]
# 普池
s5_craft_prob = pool["s5_craft_prob"] - limited_s5_craft_prob
s4_craft_prob = pool["s4_craft_prob"] - limited_s4_craft_prob
s3_craft_prob = pool["s3_craft_prob"] - limited_s3_craft_prob

# 限定/推荐几率
limited_prob = limited_s5_servant_prob + limited_s3_servant_prob + recommend_s4_servant_prob \
               + recommend_s3_servant_prob + limited_s5_craft_prob + limited_s4_craft_prob + limited_s3_craft_prob
# 限定从者几率
limited_servant_prob = limited_s5_servant_prob + limited_s3_servant_prob
# 推荐从者几率
recommend_servant_prob = recommend_s4_servant_prob + recommend_s3_servant_prob
# 限时礼装几率
limited_craft_prob = limited_s5_craft_prob + limited_s4_craft_prob + limited_s3_craft_prob

TOTAL_PROP = 1000

# 取卡池
# 从者
limited_s5_servant = pool["limited_s5_servant"]
limited_s3_servant = pool["limited_s3_servant"]
recommend_s4_servant = pool["recommend_s4_servant"]
recommend_s3_servant = pool["recommend_s3_servant"]
s5_servant = pool["s5_servant"]
s4_servant = pool["s4_servant"]
s3_servant = pool["s3_servant"]
# 礼装
limited_s5_craft = pool["limited_s5_craft"]
limited_s4_craft = pool["limited_s4_craft"]
limited_s3_craft = pool["limited_s3_craft"]
s5_craft = pool["s5_craft"]
s4_craft = pool["s4_craft"]
s3_craft = pool["s3_craft"]

pool_name = pool["pool_name"]


# gacha
@on_command('fgo', aliases=('fgo十连',), only_to_me=False)
async def gacha(session: CommandSession):
    user_id = session.ctx['user_id']
    if not util.check_interval(user_id, __module__, 60):
        session.finish('您抽的太快了，请让Madao休息一下，过几分钟后再来查吧', at_sender=True)

    at_msg = ''
    if session.ctx['message_type'] == 'group':
        at_msg = '[CQ:at,qq={}]\n'.format(str(user_id))

    at_msg += "本期卡池：" + pool_name + "\n"
    limit_chara = ""
    for c in limited_s5_servant:
        limit_chara += " " + str(c) + "★5"
    for c in limited_s3_servant:
        limit_chara += " " + str(c) + "★3"
    at_msg += "本期限定：" + limit_chara + "\n"
    recmd_chara = ""
    for c in recommend_s4_servant:
        recmd_chara += " " + str(c) + "★4"
    for c in recommend_s3_servant:
        recmd_chara += " " + str(c) + "★3"
    at_msg += "本期推荐：" + recmd_chara + "\n"

    at_msg += "本次抽卡结果：\n"

    text_result = ""

    results = gacha_ten()
    ls5_servant, ns5_servant, _ls5_craft, _ns5_craft = filter_s5(results)

    name = session.ctx['user_id']
    count, width, height, space = 0, 132, 144, 10
    background = Image.new('RGBA', (width * 5 + space, height * 2 + space), color='lavenderblush')

    for x in range(5):
        for y in range(2):
            pic = Image.open(os.path.join(res_root, results[count] + '.jpg'))
            background.paste(pic, (x * width + space, y * height + space))
            count += 1
    background.save(res_root + f'\\out\\{name}.png')

    if len(ls5_servant) == 0 and len(ns5_servant) == 0:
        text_result += "木有五星也没事，相信自己，下一发就出聊"
    elif len(ls5_servant) == 1 and len(ns5_servant) == 0:
        text_result += "本期限定get，恭喜恭喜，今天这么开心不如给大伙们发个红包吧"
    elif len(ls5_servant) == 0 and len(ns5_servant) == 1:
        text_result += "五星从者+1，感觉来了，不要停下来啊~~"
    elif len(ls5_servant) + len(ns5_servant) > 1:
        text_result += "五星数量" + str(len(ls5_servant) + len(ns5_servant)) + ", 啊这，先提前谢谢老板（伸手"
    text_result += "\n--- 抽卡形式仅为猜测，请以实际情况为准，P.S.卡池太大懒得维护了，凑合抽吧 --- "

    util.set_interval(user_id, __module__)
    await session.send(at_msg + f'[CQ:image,file=file:///{res_root}\\out\\{name}.png]\n' + text_result)


# gacha
@on_command('fgo_gacha2', aliases=('fgo来一单',), only_to_me=False)
async def gacha(session: CommandSession):
    user_id = session.ctx['user_id']
    if not util.check_interval(user_id, __module__, 60):
        session.finish('您抽的太快了，请让Madao休息一下，过几分钟后再来查吧', at_sender=True)

    at_msg = ''
    if session.ctx['message_type'] == 'group':
        at_msg = '[CQ:at,qq={}]\n'.format(str(user_id))

    at_msg += "本期卡池：" + pool_name + "\n"
    limit_chara = ""
    for c in limited_s5_servant:
        limit_chara += " " + str(c) + "★5"
    for c in limited_s3_servant:
        limit_chara += " " + str(c) + "★3"
    at_msg += "本期限定：" + limit_chara + "\n"
    recmd_chara = ""
    for c in recommend_s4_servant:
        recmd_chara += " " + str(c) + "★4"
    for c in recommend_s3_servant:
        recmd_chara += " " + str(c) + "★3"
    at_msg += "本期推荐：" + recmd_chara + "\n"

    at_msg += "本次抽卡结果：\n"

    text_result = ""

    results = []
    # 五次十连
    for _ in range(1, 5):
        results.extend(gacha_ten())
    # 六次单抽
    for _ in range(1, 6):
        results.append(gacha_one())

    ls5_servant, ns5_servant, ls5_craft, ns5_craft = filter_s5(results)
    s5_results = ls5_servant + ls5_craft + ns5_servant + ns5_craft
    logger.debug(s5_results)

    if len(s5_results) == 0:
        text_result = "好像没有五星呢，我仿佛听到了钱扔进大海的声音~~~"
    else:
        name = session.ctx['user_id']
        count, width, height, space = 0, 132, 144, 10

        w = 4
        h = math.ceil(len(s5_results) / w)

        background = Image.new('RGBA', (width * w + space, height * h + space), color='lavenderblush')

        for y in range(h):
            for x in range(w):
                if count < len(s5_results):
                    pic = Image.open(os.path.join(res_root, s5_results[count] + '.jpg'))
                    background.paste(pic, (x * width + space, y * height + space))
                    count += 1

        background.save(res_root + f'\\out\\{name}.png')

        if len(ls5_servant) == 0 and len(ns5_servant) == 0:
            text_result += "嗯？一个五星从者都没有吗"
        elif len(ls5_servant) == 1 and len(ns5_servant) == 0:
            text_result += "一般一般，世界第三~"
        elif len(ls5_servant) == 0 and len(ns5_servant) == 1:
            text_result += "五星从者+1，感觉来了，不要停下来啊~~"
        elif len(ls5_servant) + len(ns5_servant) > 1:
            text_result += "五星数量" + str(len(ls5_servant) + len(ns5_servant)) + ", 啊这，已经可以了，你已经很欧了"

        text_result += "\n--- 抽卡形式仅为猜测，请以实际情况为准，P.S.卡池太大懒得维护了，凑合抽吧 --- "
        text_result = f'[CQ:image,file=file:///{res_root}\\out\\{name}.png]\n' + text_result

        util.set_interval(user_id, __module__)

    await session.send(at_msg + text_result)


# 十连
def gacha_ten() -> List[str]:
    result = []
    # 先单抽八次
    for n in range(8):
        result.append(gacha_one())

    # 进入保底
    # 金卡位（五星: 五礼: 四星: 四礼 = 1 : 4 : 3 : 92）
    # 从者位（五星: 四星: 三星 = 1 : 3 : 96）

    # 金卡位：
    i = random.random() * 1000
    if i <= limited_s5_servant_prob:  # 五星限定从者
        result.append(random.choice(limited_s5_servant))
    elif i <= 10:  # 普池五星从者
        result.append(random.choice(s5_servant))
    elif i <= 10 + s5_craft_prob:  # 五星限定礼装
        result.append(random.choice(limited_s5_craft))
    elif i <= 50:  # 普池五星礼装
        result.append(random.choice(s5_craft))
    elif i <= 50 + recommend_s4_servant_prob:  # 四星推荐从者
        result.append(random.choice(recommend_s4_servant))
    elif i <= 80:  # 四星普通从者
        result.append(random.choice(s4_servant))
    elif i <= 80 + limited_s4_craft_prob:  # 四星限定礼装
        result.append(random.choice(limited_s4_craft))
    else:  # 四星普通礼装
        result.append(random.choice(s4_craft))

    # 从者位:
    i = random.random() * 1000
    if i <= limited_s5_servant_prob:  # 五星限定从者
        result.append(random.choice(limited_s5_servant))
    elif i <= 10:  # 普池五星从者
        result.append(random.choice(s5_servant))
    elif i <= 10 + recommend_s4_servant_prob:  # 四星推荐从者
        result.append(random.choice(recommend_s4_servant))
    elif i <= 40:  # 四星普通从者
        result.append(random.choice(s4_servant))
    elif i <= 40 + limited_s3_servant_prob:  # 三星限定从者
        result.append(random.choice(limited_s3_servant))
    elif i <= 40 + limited_s3_servant_prob + recommend_s3_servant_prob:  # 三星推荐从者
        result.append(random.choice(recommend_s3_servant))
    else:  # 三星普通从者
        result.append(random.choice(s3_servant))

    return result


# 单抽
def gacha_one() -> str:
    i = random.random() * 1000
    if i <= limited_prob:  # 出限定
        if i <= limited_servant_prob:  # 出限定从者
            if i <= limited_s5_servant_prob:  # 出限定从者
                return random.choice(limited_s5_servant)
            else:  # 出限定三星
                return random.choice(limited_s3_servant)
        elif i <= limited_servant_prob + recommend_servant_prob:
            if i <= limited_servant_prob + recommend_s4_servant_prob:  # 出推荐四星
                return random.choice(recommend_s4_servant)
            else:  # 出推荐三星
                return random.choice(recommend_s3_servant)
        else:  # 出限时礼装
            if i <= limited_prob - limited_s3_craft_prob - limited_s4_craft_prob:  # 出限时五星礼装
                return random.choice(limited_s5_craft)
            elif i <= limited_prob - limited_s3_craft_prob:  # 出限时四星礼装
                return random.choice(limited_s4_craft)
            else:  # 出限时三星礼装
                return random.choice(limited_s3_craft)
    else:  # 无限定，普通卡池取卡
        SL = TOTAL_PROP - s5_craft_prob - s4_craft_prob - s3_craft_prob
        if i <= SL:  # 普池从者
            if i <= SL - s4_servant_prob - s3_servant_prob:  # 普池五星从者
                return random.choice(s5_servant)
            elif i <= SL - s3_servant_prob:  # 普池四星从者
                return random.choice(s4_servant)
            else:  # 普池三星从者
                return random.choice(s3_servant)
        else:  # 普池礼装
            if i <= TOTAL_PROP - s4_craft_prob - s3_craft_prob:  # 普池五星礼装
                return random.choice(s5_craft)
            elif i <= TOTAL_PROP - s3_craft_prob:  # 普池四星礼装
                return random.choice(s4_craft)
            else:  # 普池三星礼装
                return random.choice(s3_craft)


# 滤出五星
def filter_s5(results):
    ls5_servant, ns5_servant, ls5_craft, ns5_craft = [], [], [], []
    for r in results:
        if r in limited_s5_servant:
            ls5_servant.append(r)
        elif r in s5_servant:
            ns5_servant.append(r)
        elif r in limited_s5_craft:
            ls5_craft.append(r)
        elif r in s5_craft:
            ns5_craft.append(r)
        else:
            pass
    return ls5_servant, ns5_servant, ls5_craft, ns5_craft
