from typing import Any, Dict

import dotenv
from pydantic import BaseModel, Json


class AppConfig(BaseModel):
    LOG_LEVEL: str
    DATABASE_URL: str
    SLACK_BOT_TOKEN: str
    SLACK_APP_TOKEN: str
    API_HOST: str
    API_PORT: int
    API_CORS_ORIGINS: Json[list[str]]
    IGNORED_EMOJIS: Json[list[str]]

    class Config:
        frozen = True


CONFIG: AppConfig
TORTOISE_ORM: dict[str, Any]


def load_config() -> AppConfig:
    return AppConfig(**dotenv.dotenv_values())


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
    for name, field_data in AppConfig.schema()["properties"].items():
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

    TORTOISE_ORM = {
        "connections": {"default": CONFIG.DATABASE_URL},
        "apps": {
            "models": {
                "models": ["src.models"],
                "default_connection": "default",
            }
        },
    }

    # Config specifically for use with Aerich
    TORTOISE_ORM_AERICH = {
        **TORTOISE_ORM,
        "apps": {
            "models": {
                "models": ["aerich.models", "src.models"],
                "default_connection": "default",
            },
        },
    }
