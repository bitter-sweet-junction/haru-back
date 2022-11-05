#!/bin/sh

# build
docker build . -t haru-back

# run
docker run \
    -d --rm \
    -p 1213:80 \
    --env-file .env \
    -v $(pwd)/data:/data \
    haru-back
