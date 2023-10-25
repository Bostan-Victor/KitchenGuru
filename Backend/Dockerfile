FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /ktbackend

WORKDIR /ktbackend

COPY . /ktbackend

ENV APP_NAME=KITCHENGURU

RUN pip install -r /ktbackend/requirements.txt

RUN chmod +x /ktbackend/conf/entrypoint.sh

CMD /ktbackend/conf/entrypoint.sh

# CMD ["gunicorn", "KitchenGuru.wsgi:application", "-b", "0.0.0.0:8000"]