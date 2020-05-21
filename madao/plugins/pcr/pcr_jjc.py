# -*- coding:utf-8 -*-
from nonebot import on_command, CommandSession


@on_command('mining', aliases=('jjc挖矿', 'pjjc挖矿', 'jjc挖矿查询', 'pjjc挖矿查询'), only_to_me=False)
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
