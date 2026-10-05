import os
import shutil
from importlib.resources import files
from pathlib import Path

import tomlkit


def get_config_path() -> Path:
    config_dir = Path(os.environ["APPDATA"]) / "rag-cli"
    config_dir.mkdir(parents=True, exist_ok=True)

    config_path = config_dir / "conf.toml"
    if not config_path.exists():

        bundled_config = files("rag_cli").joinpath("conf.toml")
        with bundled_config.open("rb") as src, open(config_path, "wb") as dst:
            shutil.copyfileobj(src, dst)

    return config_path


def get_config() -> tomlkit.TOMLDocument:
    config_path = get_config_path()
    return tomlkit.parse(config_path.read_text(encoding="utf-8"))


def save_config(config: tomlkit.TOMLDocument) -> None:
    config_path = get_config_path()
    config_path.write_text(tomlkit.dumps(config), encoding="utf-8")
    print(f"Configuration saved to {config_path}")
