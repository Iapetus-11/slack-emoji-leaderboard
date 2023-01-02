from typing import Any, Dict

import dotenv
from pydantic import BaseModel


class BotConfig(BaseModel):
    LOG_LEVEL: str
    DISCORD_BOT_TOKEN: str
    DISCORD_GUILD_ID: int
    API_ADDRESS: str
    API_AUTH: str

    class Config:
        frozen = True


CONFIG: BotConfig


def load_config() -> BotConfig:
    return BotConfig(**dotenv.dotenv_values())


def _get_field_value_or_example(field_data: Dict[str, Any]) -> object:
    if "default" in field_data:
        return str(field_data["default"])

    data_type = field_data.get("type")

    if data_type == "integer":
        return 123456

    if data_type == "number":
        return 123.456

    return data_type


def _generate_example_env():
    lines = list[str]()
    current_section = ""

    name: str
    field_data: dict[str, Any]
    for name, field_data in BotConfig.schema()["properties"].items():
        if (section := name.split("_")[0]) != current_section:
            current_section = section
            lines.append("\n")

        lines.append(f"{name}={_get_field_value_or_example(field_data)}\n")

    with open("example.env", "w+") as example_env:
        example_env.writelines(lines[1:])


if __name__ == "__main__":
    print("Generating example.env file...")
    _generate_example_env()
    print("Done!")
else:
    CONFIG = load_config()
