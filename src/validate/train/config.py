
from pydantic import Field, field_validator, ValidationError
from typing import Any
from ..types import StrictConfig
from ..transforms import TRANSFORMS

class TrainConfig(StrictConfig):
    num_epochs: int
    transforms: list[dict[str, Any]] | None = Field(default_factory=list)

    @field_validator("transforms")
    @classmethod
    def validate_transforms(cls, transforms):
        for item in transforms:
            params = item.copy()
            name = params.pop("name")
            try:
                transform_class = TRANSFORMS[name]
            except KeyError:
                supported = ", ".join(sorted(TRANSFORMS))
                raise ValueError(
                    f"Unsupported transform: {name!r}. Supported types: {supported}"
                ) from None
            
            try:
                transform_class(**params)
            except ValidationError as exc:
                raise ValueError(
                    f"Invalid config for transform {name!r}: {exc}"
                ) from exc
        return transforms
