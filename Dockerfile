FROM python:3.11-slim
WORKDIR /docker/telegramqrbot
COPY requirements.txt /docker/telegramqrbot
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /docker/telegramqrbot

CMD ["python3", "src/main.py"]