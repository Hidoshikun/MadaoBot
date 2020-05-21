# -*- coding:utf-8 -*-
import re
import json
import time
import os
from nonebot import on_command, CommandSession
import nonebot
from madao import aiorequests, util

bot = nonebot.get_bot()

# 竞技场查询用key
KEY = bot.config.JJC_KEY

# 名字配置
cfg_root = os.path.join(bot.config.CONFIG_DIR, 'pcr.json')
config = util.load_config(cfg_root)
name_config = config["name_config"]

# 查询cd记录
interval_dict = {}


def check_interval(user_id):
    if user_id not in interval_dict or int(time.time()) - interval_dict[user_id] >= 120:
        return True
    else:
        return False


def set_interval(user_id):
    interval_dict[user_id] = int(time.time())


@on_command('jjc_search', aliases=('怎么拆', 'b怎么拆', '竞技场查询', '如何拆'), only_to_me=False)
async def jjc_search(session: CommandSession):
    user_id = session.ctx['user_id']
    if not check_interval(user_id):
        session.finish('您查询的太快了，请让Madao休息一下，过几分钟后再来查吧~', at_sender=True)

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

    result = await do_search(id_list)
    if session.ctx['message_type'] == 'group':
        at_msg = '[CQ:at,qq={}]'.format(str(user_id))
    else:
        at_msg = "您"

    msg = "已为骑士君" + at_msg + "查询到排名前五的解法：\n"
    for r in result:
        msg += r.to_text() + "\n"

    msg += "Madao当前仅支持国服查询，Powered by pcrdfans.com"
    set_interval(user_id)
    await session.send(msg)


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

# if __name__ == "__main__":
#     defend = "狐狸 望 猫剑 黑骑 布丁"
#     print("防守方： " + defend)
#     output = do_search(user_input(defend))
#     parse_result(output)
