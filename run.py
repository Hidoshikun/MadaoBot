import madao
import config

bot = madao.init(config)
app = bot.asgi

if __name__ == '__main__':
    bot.run()
