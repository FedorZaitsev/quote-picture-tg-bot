FROM ubuntu:latest

RUN apt-get update -y && apt-get install -y python3.11 python3.11-distutils

RUN apt-get install -y vim

RUN apt-get install -y python3-pip

RUN pip install telebot && pip install urllib3 && pip install pyTelegramBotAPI

CMD ["python3", "data/tgbot/main.py"]