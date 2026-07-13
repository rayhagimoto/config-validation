# Config Validation

This repo demonstrates Pydantic's capability to validate complex YAML schema.

In particular, it shows how methods in a registry (`TRANSFORMS`) can validate the schema against their `__init__` args by applying the `@validate_call` decorator. In addition, we show that this approach is flexible to lists which are allowed to have an arbitrary number of [`transforms`](src/validate/transforms.py)

The [demo](test.ipynb) shows what the imported config looks like and how the params are built.

## Define a transform

Register a transform class under the name used in YAML. `@validate_call` validates
the YAML parameters against the type annotations on `__init__`.

```python
from pydantic import validate_call

@register_transform("gaussian_smoothing_1d")
class GaussianSmoothing1d(Transform):
    @validate_call
    def __init__(self, sigma: float):
        self.sigma = sigma

    def __call__(self, X):
        # Apply Gaussian smoothing using self.sigma.
        return X
```

This transform is configured as:

```yaml
- name: gaussian_smoothing_1d
  sigma: 0.158
```

## Validate a transform list

Each transform entry may use a different constructor and parameter shape. The
raw type is therefore `dict[str, Any]`; the field validator selects the class
from the registry, then validates its parameters by constructing it.

```python
from typing import Any

from pydantic import Field, ValidationError, field_validator

class TrainConfig(StrictConfig):
    num_epochs: int
    transforms: list[dict[str, Any]] = Field(default_factory=list)

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
```
