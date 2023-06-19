FROM python:3.11.4-alpine

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry

COPY . /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

ENTRYPOINT [ "poetry", "run", "python", "manage.py" ]

CMD [ "runserver", "0.0.0.0:8000"]