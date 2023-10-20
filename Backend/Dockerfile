FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code

WORKDIR /code

COPY . /code

ADD .env /code/.env

ENV APP_NAME=KITCHENGURU


RUN pip install -r /code/requirements.txt

RUN chmod +x /code/conf/entrypoint.sh
# CMD ["/code/conf/entrypoint.sh"]
CMD gunicorn KitchenGuru.wsgi:application -b 0.0.0.0:8000

