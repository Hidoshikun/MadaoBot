from datetime import datetime
import nonebot
from nonebot import scheduler
from nonebot import logger
from bs4 import BeautifulSoup
import pytz
import requests
import json
from aiocqhttp.exceptions import Error as CQHttpError

accounts = [
    {'name': '最终幻想14', 'uid': '1797798792', 'container_id': '1076031797798792'},
    {'name': '命运-冠位指定', 'uid': '5732523783', 'container_id': '1076035732523783'},
    {'name': '明日方舟Arknights', 'uid': '6279793937', 'container_id': '1076036279793937'},
    {'name': '公主连结ReDive', 'uid': '6603867494', 'container_id': '1076036603867494'},
    {'name': '贞德蘸酱 ', 'uid': '6305490806', 'container_id': '1076036305490806'},
]

temp_info = {
    '最终幻想14': 0,
    '命运-冠位指定': 0,
    '明日方舟Arknights': 0,
    '公主连结ReDive': 0,
    '贞德蘸酱 ': 0,
}

push_group = [917126871, 953877394]


@scheduler.scheduled_job('interval', minutes=1)
async def weibo_poller():
    bot = nonebot.get_bot()
    for account in accounts:
        try:
            result = await poll_new_weibo(account['name'], int(account['uid']), int(account['container_id']))
            if len(result) != 0:
                logger.info(f"成功获取@{account}的新微博")
                for group in push_group:
                    try:
                        await bot.send_group_msg(group_id=group,
                                                 message=result[0])
                    except CQHttpError:
                        pass
            else:
                logger.info(f"未检测到@{account}的新微博")
        except Exception as e:
            logger.exception(e)
            logger.error(f"获取@{account}的微博时出现异常{type(e)}")


async def poll_new_weibo(name: str, uid: int, container_id: int):
    url = r'https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid={}'.format(uid, container_id)
    logger.debug(url)
    s = requests.post(url=url, timeout=15)
    jdata = json.loads(s.text)
    max_id = 0
    if jdata["ok"] == 1:
        for card in jdata["data"]["cards"]:
            if 'mblog' in card:
                m_blog = card['mblog']
                max_id = max(int(m_blog['id']), max_id)

        for card in jdata["data"]["cards"]:
            if 'mblog' in card and int(card['mblog']['id']) == max_id:
                blog_id = int(card['mblog']['id'])
                if blog_id <= temp_info[name] or temp_info[name] == 0:
                    temp_info[name] = max(blog_id, temp_info[name])
                    return []
                else:
                    m_blog = card['mblog']
                    bs = BeautifulSoup(m_blog["text"], "html.parser")
                    if "original_pic" in m_blog.keys():
                        text = "{}\n{}".format(
                            "{}\'s Weibo:\n========".format(name),
                            bs.get_text().replace("\u200b", "").strip()
                        )
                        msg = [
                            {"type": "text", "data": {"text": text}, },
                            {"type": "image", "data": {"file": m_blog["original_pic"]}, }
                        ]
                    else:
                        msg = "{}\n{}".format(
                            "{}\'s Weibo:\n========".format(name),
                            bs.get_text().replace("\u200b", "").strip(),
                        )
                    temp_info[name] = max(blog_id, temp_info[name])
                    return [msg]
