from pathlib import Path
from yaml import safe_load
from .types import StrictConfig
from .train.config import TrainConfig

__all__ = [
    "load_config",
]

class Config(StrictConfig):
    name: str
    train: TrainConfig

def _load_raw_config(path: str | Path) -> dict:
    with open(path, "r") as f:
        params = safe_load(f)
    return dict(params)

def load_config(path: str | Path) -> Config:
    "Loads config from YAML, with schema-validation."
    raw_config = _load_raw_config(path)
    return Config(**raw_config)

