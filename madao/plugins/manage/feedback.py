from nonebot import on_command, CommandSession, permission as perm
import time

# 查询cd记录
interval_dict = {}


def check_interval(user_id):
    if user_id not in interval_dict or int(time.time()) - interval_dict[user_id] >= 86400:
        return True
    else:
        return False


def set_interval(user_id):
    interval_dict[user_id] = int(time.time())


@on_command('留言', permission=perm.GROUP)
async def feedback(session: CommandSession):
    user_id = session.ctx['user_id']
    at_msg = '[CQ:at,qq={}]'.format(str(user_id))
    if not check_interval(user_id):
        session.finish(at_msg + '每天只能反馈一次哦，明天再来吧', at_sender=True)

    to_user = session.bot.config.SUPERUSERS[0]
    text = session.current_arg
    if not text:
        await session.send(f"留言[空格]后输入您要反馈的内容", at_sender=True)
    else:
        set_interval(user_id)

        await session.bot.send_private_msg(self_id=session.ctx['self_id'], user_id=to_user,
                                           message=f'Q{user_id}@群{session.ctx["group_id"]}\n{text}')
        await session.send(f'您的留言已发送！\n=======\n{text}', at_sender=True)
