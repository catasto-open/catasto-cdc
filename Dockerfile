FROM python:3.10-slim-bullseye

SHELL ["/bin/bash", "-c"]
WORKDIR /project

ADD cdc /project/cdc
COPY pyproject.toml /project/

RUN pip install --no-cache-dir .

CMD ["faststream", "run", "--workers", "1", "app.cdc:app"]
