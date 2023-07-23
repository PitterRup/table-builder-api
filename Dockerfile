FROM python:3.11-bullseye

WORKDIR /usr/src/app

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/root/.local/bin"

COPY poetry.lock pyproject.toml /usr/src/app/

RUN poetry install

CMD ["poetry", "run", "table_builder_api/manage.py", "runserver", "0.0.0.0:8000"]
