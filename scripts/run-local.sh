#!/bin/sh

# build
docker build . -t haru-back

# run
docker run \
    -p 1213:80 \
    --env-file .env \
    haru-back
