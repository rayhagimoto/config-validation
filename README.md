# Config Validation

This repo demonstrates Pydantic's capability to validate complex YAML schema.

In particular, it shows how methods in a registry (`TRANSFORMS`) can validate the schema against their `__init__` args by applying the `@validate_call` decorator. In addition, we show that this approach is flexible to lists which are allowed to have an arbitrary number of [`transforms`](src/validate/transforms.py)

The [demo](test.ipynb) shows what the imported config looks like and how the params are built.
