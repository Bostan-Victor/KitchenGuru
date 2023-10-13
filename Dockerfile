FROM python:3.11.6

RUN mkdir /code/
COPY requirements.txt /code/requirements.txt

WORKDIR /code/

ADD . /code/
ADD .env.docker /code/.env

ENV APP_NAME=KITCHENGURU

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD gunicorn KitchenGuru.wsgi:application -b 0.0.0.0:8000

