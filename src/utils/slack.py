from typing import Any, Generator


def get_block_emojis(elements: list[dict[str, Any]]) -> Generator[str, None, None]:
    for el in elements:
        # Ensure block element is an emoji and is a custom one
        if el["type"] == "emoji" and not el.get("unicode"):
            yield el["name"]

        if sub_elements := el.get("elements"):
            yield from get_block_emojis(sub_elements)
