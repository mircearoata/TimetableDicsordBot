FROM python:3.8.3

COPY . /app

WORKDIR /app/bot

RUN pip install -r ../requirements.txt

VOLUME /app/config

CMD python ./bot.py