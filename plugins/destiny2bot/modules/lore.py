from json import dumps

from httpx import AsyncClient
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from nonebot.params import State
from nonebot.typing import T_State
from zhconv import convert

lore = on_command("吹逼", priority=1)


@lore.handle()
async def handle_args(bot: Bot, event: MessageEvent, state: T_State = State()) -> None:
    from .. import plugin_config

    args: list[MessageSegment] = state.get("_prefix", {}).get("command_arg")
    lore_name: str = args[0].data.get("text") if args else ""
    lore_url = f"{plugin_config.d2bot_manifest_api}/lore/"
    async with AsyncClient() as client:
        if not lore_name:
            chs_resp = await client.get(lore_url, params={"lang": "zh-chs"})
        else:
            lore_name_chs = convert(lore_name, "zh-cn")
            lore_name_cht = convert(lore_name, "zh-tw")
            print(
                f"Received lore name: {lore_name}, "
                f"chs: {lore_name_chs}, "
                f"cht: {lore_name_cht} "
            )
            chs_resp = await client.get(
                lore_url, params={"title": lore_name_chs, "lang": "zh-chs"}
            )
            cht_resp = await client.get(
                lore_url, params={"title": lore_name_cht, "lang": "zh-cht"}
            )
    if chs_resp.status_code == 200:
        data = chs_resp.json()
        await lore.finish(
            f"""《{data.get("title")}》"""
            f"""{f"——{data.get('subtitle')}" if data.get('subtitle') else ''}\n"""
            f"""{data.get('content')}"""
        )
    elif cht_resp.status_code == 200:
        data = cht_resp.json()
        await lore.finish(
            f"""《{data.get("title")}》"""
            f"""{f"——{data.get('subtitle')}" if data.get('subtitle') else ''}\n"""
            f"""{data.get('content')}"""
        )
    else:
        await lore.finish("吹不出来")
