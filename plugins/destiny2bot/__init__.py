import nonebot
from .config import Config
from . import modules

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
