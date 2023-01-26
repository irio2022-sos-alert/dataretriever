#!/bin/bash

readonly topic="$1"

gcloud pubsub topics create $topic --message-encoding=json || true
