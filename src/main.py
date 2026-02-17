import importlib
import json
import os
from typing import TYPE_CHECKING

from color import COLOR_MAP
from theme import waguri

if TYPE_CHECKING:
    from types import ModuleType


def get_filename() -> list[str]:
    filenames: list[str] = []
    for filename in os.listdir("src/language"):
        if filename.endswith(".py"):
            filenames.append(filename)
    return filenames


def get_module(filename: str) -> "ModuleType":
    module_name = f"language.{filename[:-3]}"
    module = importlib.import_module(module_name)
    return module


def append_data(theme: dict, module: "ModuleType") -> None:
    if hasattr(module, "semantic_token"):
        theme["semanticTokenColors"].update(module.semantic_token)
    for attr, target in COLOR_MAP.items():
        if hasattr(module, attr):
            new_scopes = getattr(module, attr)
            for s in new_scopes:
                if s not in target["scope"]:
                    target["scope"].append(s)  # type: ignore
            if target not in theme["tokenColors"]:
                theme["tokenColors"].append(target)


def build_json(theme: dict) -> None:
    filenames: list[str] = get_filename()
    for filename in filenames:
        module: ModuleType = get_module(filename)
        append_data(theme, module)
    theme_path = "themes/Waguri-color-theme.json"
    with open(theme_path, "w") as f:
        json.dump(theme, f, indent=4)


if __name__ == "__main__":
    theme = waguri
    build_json(theme)
