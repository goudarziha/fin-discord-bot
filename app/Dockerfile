FROM python:3.9

COPY requirements.txt /opt/bot/requirements.txt
WORKDIR /opt/bot
RUN pip install -r requirements.txt
COPY . /opt/bot

CMD ["python", "./bot.py"]
