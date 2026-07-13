from pathlib import Path

import pytest
from pydantic import ValidationError

from validate import load_config


CONFIG_DIR = Path(__file__).parent.parent / "config"


@pytest.mark.parametrize(
    "filename",
    [
        "invalid_1.yaml",
        "invalid_2.yaml",
        "invalid_3.yaml",
    ],
)
def test_invalid_config(filename):
    "Verify that invalid configs fail"
    with pytest.raises(ValidationError):
        load_config(CONFIG_DIR / filename)

@pytest.mark.parametrize(
    "filename",
    [
        "valid_1.yaml",
        "valid_2.yaml",
    ],
)
def test_valid_config(filename):
    "Verify that invalid configs fail"
    config = load_config(CONFIG_DIR / filename)
    assert config.train.num_epochs == 10
