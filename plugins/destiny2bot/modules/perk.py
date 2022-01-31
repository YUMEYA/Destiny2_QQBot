from json import dumps

from httpx import AsyncClient
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from nonebot.params import State
from nonebot.typing import T_State
from zhconv import convert

perk = on_command("perk", priority=1)


@perk.handle()
async def handle_args(bot: Bot, event: MessageEvent, state: T_State = State()) -> None:
    args: list[MessageSegment] = state.get("_prefix", {}).get("command_arg")
    weapon_name = args[0].data.get("text")
    state["weapon_name"] = weapon_name


@perk.got("weapon_name", prompt="请输入装备名称")
async def search_weapon(
    bot: Bot, event: MessageEvent, state: T_State = State()
) -> None:
    weapon_name = state["weapon_name"]
    weapon_name_chs = convert(weapon_name, "zh-cn")
    weapon_name_cht = convert(weapon_name, "zh-tw")
    print(
        f"Received weapon name: {weapon_name}, "
        f"chs: {weapon_name_chs}, "
        f"cht: {weapon_name_cht} "
    )

    from .. import plugin_config

    weapon_url = f"{plugin_config.d2bot_manifest_api}/weapon/"
    async with AsyncClient() as client:
        chs_resp = await client.get(
            weapon_url, params={"name": weapon_name_chs, "lang": "zh-chs"}
        )
        cht_resp = await client.get(
            weapon_url, params={"name": weapon_name_cht, "lang": "zh-cht"}
        )
    if chs_resp.status_code != 200 and cht_resp.status_code != 200:
        await perk.reject(f"未找到装备：{weapon_name}")
    elif cht_resp.status_code == 200:
        await perk.finish(f"{dumps(cht_resp.json(),indent=2,ensure_ascii=False)}")
    elif chs_resp.status_code == 200:
        await perk.finish(f"{dumps(chs_resp.json(),indent=2,ensure_ascii=False)}")
