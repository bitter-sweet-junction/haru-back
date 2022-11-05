#!/bin/sh

docker stop $(docker ps -q --filter ancestor=haru-back)
