#!/bin/sh

if [ "$#" -ne 1 ]
then
  echo "Usage: $0 <TAG NAME>"
  exit 1
fi

IMAGE_NAME=gcr.io/haru-today/haru-back:$1

# build
docker build . -t $IMAGE_NAME

# upload
docker push $IMAGE_NAME

# deploy cloud run
gcloud run deploy haru-back \
    --image=$IMAGE_NAME \
    --allow-unauthenticated \
    --port=80 \
    --service-account=haru-backend@haru-today.iam.gserviceaccount.com \
    --set-env-vars=$(cat .env | tr "\n" ",") \
    --region=asia-northeast3 \
    --project=haru-today
