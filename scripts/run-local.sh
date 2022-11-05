#!/bin/sh

# build
docker build . -t haru-back

# run
docker run \
    --rm \
    -p 1213:80 \
    --env-file .env \
    -e GOOGLE_APPLICATION_CREDENTIALS=/data/credentials.json \
    -v $(pwd)/data:/data \
    haru-back
