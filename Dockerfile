FROM python:3

WORKDIR /app

COPY poetry.lock pyproject.toml /

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /app/

ENV PYTHONPATH=/app/api/app/botForward_api

RUN chmod +x run.sh

ENTRYPOINT [ "./run.sh" ]