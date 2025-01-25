FROM python:3.12
WORKDIR /docker/telegramqrbot
COPY requirements.txt /docker/telegramqrbot
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /docker/telegramqrbot

CMD ["python3", "src/app.py"]