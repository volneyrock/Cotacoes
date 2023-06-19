FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry

COPY . /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

ENTRYPOINT [ "poetry", "run"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]