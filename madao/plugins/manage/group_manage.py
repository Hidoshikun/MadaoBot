from nonebot import session, CommandSession
from madao.dao import GroupDao


# 命令启用检查
def check_group_command(group_id, command):
    gd = GroupDao()
    group = gd.find_one(group_id)
    if command in group['disable_command']:
        return False
    else:
        return True


def check_blacklist():
    return False
