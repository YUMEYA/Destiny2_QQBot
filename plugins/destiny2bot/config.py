from pydantic import BaseSettings


class Config(BaseSettings):

    d2bot_bungie_api_key: str = "default"
    d2bot_manifest_api: str = "default"

    class Config:
        extra = "ignore"
