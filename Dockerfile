FROM python:3.8.3

COPY . ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app

VOLUME /app/config

CMD python ./bot/bot.py