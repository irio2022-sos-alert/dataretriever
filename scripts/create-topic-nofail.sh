#!/bin/bash

readonly topic="$1"
readonly schema="$2"
gcloud pubsub topics create $topic --message-encoding=json --schema=$schema || true
