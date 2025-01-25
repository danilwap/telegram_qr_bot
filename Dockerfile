FROM python:3.12
WORKDIR /docker/telegramqrbot/src
COPY requirements.txt /docker/telegramqrbot/src
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /docker/telegramqrbot/src

ENTRYPOINT ["top", "-b"]