#!/bin/bash

echo "Start deploy"

docker stop qr_bot
echo "Bot stopped"

yes | docker image prune --all
yes | docker system prune -a
echo "there was clear cache"

docker build -t qr_bot .
echo "image created"


docker run --name qr_bot -d qr_bot
echo "bot started"
