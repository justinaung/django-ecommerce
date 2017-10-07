FROM python:3.6.1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y \
    && pip3 install pipenv uwsgi

WORKDIR /code

COPY Pipfile Pipfile.lock manage.py ./

RUN pipenv install --system --deploy

EXPOSE 8000

COPY django_ecommerce ./django_ecommerce
COPY static ./static
COPY templates ./templates
