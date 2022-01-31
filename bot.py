import nonebot
from nonebot.adapters.cqhttp import Adapter as CQHTTPBot

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(CQHTTPBot)
nonebot.load_builtin_plugins("echo")
nonebot.load_plugins("plugins")

if __name__ == "__main__":
    nonebot.run()
