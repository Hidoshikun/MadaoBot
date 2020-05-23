# -*- coding:utf-8 -*-
import re
import json
import time
import os
from nonebot import on_command, CommandSession, logger
from aiocqhttp.exceptions import Error as CQHttpError
import nonebot
from madao import aiorequests, util

bot = nonebot.get_bot()

# 竞技场查询用key
KEY = bot.config.JJC_KEY

# 名字配置
cfg_root = os.path.join(bot.config.CONFIG_DIR, 'pcr.json')
config = util.load_config(cfg_root)
name_config = config["name_config"]
__module__ = "pcr_jjc"


@on_command('mining', aliases=('挖矿', 'jjc挖矿', 'pjjc挖矿', 'jjc挖矿查询', 'pjjc挖矿查询'), only_to_me=False)
async def arena_diamond(session: CommandSession):
    rank = int(session.current_arg_text.strip())
    if rank > 15000:
        amount = 42029
    elif rank > 12000:
        amount = (rank / 100 - 120) * 45 + 40679
    elif rank > 11900:
        amount = 40599
    elif rank > 7999:
        amount = (rank / 100 - 80) * 95 + 36799
    elif rank > 4000:
        amount = (rank - 4001) + 32800
    elif rank > 2000:
        amount = (rank - 2001) * 3 + 26800
    elif rank > 1000:
        amount = (rank - 1001) * 5 + 21800
    elif rank > 500:
        amount = (rank - 501) * 7 + 18300
    elif rank > 200:
        amount = (rank - 201) * 13 + 14400
    elif rank > 100:
        amount = (rank - 101) * 35 + 10900
    elif rank > 10:
        amount = (rank - 11) * 60 + 5500
    elif rank > 0:
        amount = (rank - 1) * 550
    else:
        amount = 0
    messages = "剩余钻石：" + str(int(amount))
    await session.send(messages, at_sender=True)


class Chara(object):
    def __init__(self, chara_id, chara_name, star, equip):
        self.chara_id = chara_id
        self.chara_name = chara_name
        self.star = star
        self.equip = equip

    def to_text(self):
        return self.chara_name + "★" + str(self.star)


class FindResult(object):
    def __init__(self, chara_list, up, down):
        self.chara_list = chara_list
        self.up = up
        self.down = down

    def to_text(self):
        text = ""
        for c in self.chara_list:
            text += c.to_text() + " "
        return text + "  赞👍:" + str(self.up) + " " + "踩👎:" + str(self.down)


@on_command('jjc_search', aliases=('怎么拆', 'b怎么拆', '竞技场查询', '如何拆'), only_to_me=False)
async def jjc_search(session: CommandSession):
    user_id = session.ctx['user_id']
    if not util.check_interval(user_id, __module__, 60):
        session.finish('您查询的太快了，请让Madao休息一下，过几分钟后再来查吧', at_sender=True)

    name_list = session.current_arg_text.strip()
    name_list = re.sub(r'[?？，,_]', ' ', name_list)
    name_list = name_list.split()
    if 0 >= len(name_list):
        session.finish('请输入防守方角色，用空格隔开', at_sender=True)
    if 5 < len(name_list):
        session.finish('编队不能多于5名角色', at_sender=True)

    it = []
    id_list = []
    for i in name_config.values():
        it += i
    for n in name_list:
        if n not in it:
            session.finish(f'Madao暂时不知道{n}是谁哦，请换个名称查询', at_sender=True)
        for i, j in name_config.items():
            if n in j:
                id_list.append(int(i))
    for i in id_list:
        if id_list.count(i) >= 2:
            session.finish(f'查询列表中有重复的角色 {name_config[str(i)][1]}，请重新查询', at_sender=True)

    try:
        result = await do_search(id_list)
        if not result:
            await session.send('好像没有找到解法，请开动想象力自由发挥吧', at_sender=True)
        else:
            if session.ctx['message_type'] == 'group':
                at_msg = '[CQ:at,qq={}]'.format(str(user_id))
            else:
                at_msg = "您"

            msg = "当前防守阵容：" + str([id2name(i) for i in id_list]) + "\n"
            msg += "已为骑士君" + at_msg + "查询到排名前五的解法：\n"
            for r in result:
                msg += r.to_text() + "\n"

            msg += "Madao当前仅支持国服查询，Powered by pcrdfans.com"
            util.set_interval(user_id, __module__)
            await session.send(msg)
    except Exception as e:
        msg = "Error: {}".format(type(e))
        await session.send(msg)


# id>>>name
def id2name(chara_id):
    return name_config[str(chara_id)][1]


# search
async def do_search(id_list):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'authorization': KEY}
    payload = {
        "_sign": "a",
        "def": id_list,
        "nonce": "a",
        "page": 1,
        "sort": 1,
        "region": 2,  # 默认B服
        "ts": int(time.time())
    }
    url = 'https://api.pcrdfans.com/x/v1/search'
    r = await aiorequests.post(url, headers=header, data=json.dumps(payload))
    data = await r.json()
    data = data["data"]["result"]
    results = []
    for d in data:
        akt = d["atk"]
        chara_list, up, down = [], 0, 0
        for a in akt:
            chara_list.append(Chara(chara_id=a["id"], chara_name=id2name(a["id"]), star=a["star"], equip=a["equip"]))
        up = d["up"]
        down = d["down"]
        results.append(FindResult(chara_list=chara_list, up=up, down=down))

    return results[:5]


def parse_result(results):
    for r in results:
        print(r.to_text())
