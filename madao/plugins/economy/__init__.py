from nonebot import on_command, CommandSession


@on_command('sign', aliases=('签到',), only_to_me=False)
async def gacha(session: CommandSession):
    await session.send("ok")
