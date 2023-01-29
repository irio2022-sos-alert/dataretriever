# Dataretriever

In this repo we extracted the part of the system that is responsible for pinging services, as well as checking if any service unavailability time is greater than its alerting window.

- ### Whistleblower

- ### Dataretriever

- ### Parser

---

## Local setup

One has to define following env variables (example of an .env file, specific values may differ):

```bash
INSTANCE_UNIX_SOCKET=xxxxxxxx
INSTANCE_CONNECTION_NAME=xxxxxxxx
DB_NAME=alerts
DB_USER=postgres
DB_PASS=xxxxxxxx
DB_PORT=5432
PROJECT_ID=xxxxxxxx
TOPIC_ID=xxxxxxxx
ALERTMANAGER_ENDPOINT=xxxxxxxxxx
WB_ENDPOINT=xxxxxxxxxx
DR_ENDPOINT=xxxxxxxxxx
```

### Build

```bash
docker build dataretriever-app -t dataretriever-app:latest
docker build whistleblower-app -t whistleblower-app:latest
docker build wb-receiver -t wb-receiver:latest
```

### Run

```
docker run -d -p 50051:50051  --env-file .env dataretriever-app:latest
docker run -d -p 50052:50052  --env-file .env whistleblower-app:latest
docker run -d -p 50053:50053  --env-file .env wb-receiver:latest
```

---

## Cloud run setup

Env variables for docker containers:

```yaml
INSTANCE_UNIX_SOCKET: xxxxxxxx
INSTANCE_CONNECTION_NAME: xxxxxxxx
DB_NAME: alerts
DB_USER: postgres
DB_PASS: xxxxxxxx
DB_PORT: 5432
PROJECT_ID: xxxxxxxx
TOPIC_ID: xxxxxxxx
ALERTMANAGER_ENDPOINT: xxxxxxxxxx
WB_ENDPOINT: xxxxxxxxxx
DR_ENDPOINT: xxxxxxxxxx
```

Env variables for deployment:

```bash
GCP_PROJECT_ID=xxx # Google cloud project id e.g. cloudruntest-123456
DATARETRIEVER_IMAGE_NAME
WHISTLEBLOWER_IMAGE_NAME
WB_RECEIVER_IMAGE_NAME
GCP_DATARETRIEVER_APP_NAME
GCP_WHISTLEBLOWER_APP_NAME
GCP_WB_RECEIVER_APP_NAME
```

### Build

Build docker images and push them to the container registry:

```bash
./scripts/b-docker.sh datamanager $DATAMANAGER_IMAGE_NAME
./scripts/b-docker.sh datamanager-api $DATAMANAGER_API_IMAGE_NAME
```

### Deploy

When deploying for the first time there are a few caveats:

- We cannot deduce endpoints of each service before they are deployed for the first time.
  Hence, we will need to update those values after first failed deployment.
- We have to set necessary secrets/env variables for each service. Next revisions will inherit those variables, so it is only one time hassle.

```bash
gcloud run deploy $GCP_DATARETRIEVER_APP_NAME \
--image $DATARETRIEVER_IMAGE_NAME \
--region europe-north1 \
--platform managed \
--allow-unauthenticated \
--env-vars-file .env.yaml \
--add-cloudsql-instances=INSTANCE_CONNECTION_NAME
```

```bash
gcloud run deploy $GCP_WHISTLEBLOWER_APP_NAME \
--image $WHISTLEBLOWER_IMAGE_NAME \
--region europe-north1 \
--platform managed \
--allow-unauthenticated \
--env-vars-file .env.yaml \
--add-cloudsql-instances=INSTANCE_CONNECTION_NAME
```

```bash
gcloud run deploy $GCP_WB_RECEIVER_APP_NAME \
--image $WB_RECEIVER_IMAGE_NAME \
--region europe-north1 \
--platform managed \
--allow-unauthenticated \
--env-vars-file .env.yaml \
--add-cloudsql-instances=INSTANCE_CONNECTION_NAME
```
