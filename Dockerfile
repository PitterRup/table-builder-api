FROM python:3.11-bullseye

WORKDIR /usr/src/app/table_builder_api

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/root/.local/bin"

COPY table_builder_api/poetry.lock table_builder_api/pyproject.toml /usr/src/app/table_builder_api/

RUN poetry install

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
