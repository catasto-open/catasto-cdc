from pathlib import Path

from faststream.asyncapi.generate import get_app_schema  # type: ignore

from app.cdc import router

schema = get_app_schema(router).to_yaml()

with Path("asyncapi.yaml").open("w") as f:
    f.write(schema)
