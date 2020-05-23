import time
import hashlib
import random
import string
from urllib.parse import quote
from typing import Optional

from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import render_expression
from madao import aiorequests
import nonebot
from nonebot import logger

bot = nonebot.get_bot()

EXPR_DONT_UNDERSTAND = (
    '出了点问题，先别聊了QAQ',
)


@on_command('tuling')
async def tuling(session: CommandSession):
    message = session.state.get('message')

    at_msg = ''
    if session.ctx['message_type'] == 'group':
        at_msg = '[CQ:at,qq={}] '.format(str(session.ctx['user_id']))

    reply = await get_content(message.strip())

    if reply:
        await session.send(at_msg + escape(reply))
    else:
        await session.send(render_expression(EXPR_DONT_UNDERSTAND))


@on_natural_language
async def _(session: NLPSession):
    return IntentCommand(60.0, 'tuling', args={'message': session.msg_text})


def curlmd5(src):
    m = hashlib.md5(src.encode('UTF-8'))
    # 将得到的MD5值所有字符转换成大写
    return m.hexdigest().upper()


def get_params(message):
    # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）
    t = time.time()
    time_stamp = str(int(t))
    # 请求随机字符串，用于保证签名不可预测
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    # 应用标志，这里修改成自己的id和key
    app_id = bot.config.TENCENT_CHAT_APPID
    app_key = bot.config.TENCENT_CHAT_KEY
    params = {'app_id': app_id,
              'question': message,
              'time_stamp': time_stamp,
              'nonce_str': nonce_str,
              'session': '10000'
              }
    sign_before = ''
    # 要对key排序再拼接
    for key in sorted(params):
        # 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。
        sign_before += '{}={}&'.format(key, quote(params[key], safe=''))

    # 将应用密钥以app_key为键名，拼接到字符串sign_before末尾
    sign_before += 'app_key={}'.format(app_key)
    # 对字符串sign_before进行MD5运算，得到接口请求签名
    sign = curlmd5(sign_before)
    params['sign'] = sign
    return params


async def get_content(message: str) -> Optional[str]:
    if not message:
        return None
    # 聊天的API地址
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
    # 获取请求参数
    message = message.encode('utf-8')
    payload = get_params(message)
    r = await aiorequests.post(url, data=payload)
    data = await r.json()
    return data["data"]["answer"]
