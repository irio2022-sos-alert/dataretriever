#!/bin/bash

readonly app_name="$1"
readonly image_name="$2"

gcloud run deploy $app_name \
--image $image_name \
--region europe-north1 \
--platform managed \
--allow-unauthenticated \
--update-env-vars KEY1=1,KEY2=VALUE2
