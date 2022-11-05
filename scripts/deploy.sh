#!/bin/sh

if [ "$#" -ne 1 ]
then
  echo "Usage: $0 <TAG NAME>"
  exit 1
fi

IMAGE_NAME=us.gcr.io/junction-hack22esp-7022/haru-back:$1

# build
docker build . -t $IMAGE_NAME

# upload
docker push $IMAGE_NAME

# deploy cloud run
gcloud run deploy haru-back \
    --image=$IMAGE_NAME \
    --allow-unauthenticated \
    --port=80 \
    --service-account=haru-backend@junction-hack22esp-7022.iam.gserviceaccount.com \
    --set-env-vars=$(cat .env | tr "\n" ",") \
    --region=us-central1 \
    --project=junction-hack22esp-7022
