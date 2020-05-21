from nonebot import on_command, CommandSession

MANUAL = '''
- Madao使用说明 -
通用功能（带/的为命令）：
- /彩虹屁  彩虹屁
- /色图  来点色图
- /抽签  浅草寺抽签
- /晚安  深夜福利
- 聊天功能  直接@机器人进行聊天
- 复读  自动复读
- 开发者留言  群内@机器人并输入"留言 留言内容"
PCR功能：
- /pcr图书馆  pcr图书馆
- /pcr十连  pcr十连
- /来一井  来一井
- /jjc挖矿+排名  挖矿查询 示例: jjc挖矿 100
- /怎么拆+阵容  竞技场查询 示例: 怎么拆 狐狸 猫剑 偶像 黑骑 布丁
FGO功能：
- /fgo十连  fgo十连
- /fgo来一单  fgo十连
FF14功能：
- /暖暖  本周暖暖作业
暂不能自主开启的功能：
- 微博订阅推送
- 舰C舰娘整点报时
TODOLIST: FF14 - dps查询 明日方舟 - 抽卡 公招查询
- 更多功能开发中... -
'''.strip()


@on_command('help', aliases=('manual', '帮助', '说明', '使用说明', '幫助', '說明', '使用說明', '菜单', '菜單'), only_to_me=False)
async def send_help(session):
    await session.send(MANUAL)
