#!/bin/bash

# TO RUN LOCAL VALIDATIONS OF THE SYSTEMS, YOU CAN RUN...


# 1) Execute DynamoDB locally with the help of:
# --> https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html
cd local-tests
docker-compose up

# 2) Add the necessary environment variables for the tests:
export AWS_ACCESS_KEY_ID=DUMMYIDEXAMPLE
export AWS_SECRET_ACCESS_KEY=DUMMYEXAMPLEKEY
export AWS_DEFAULT_REGION=us-east-1
export ENDPOINT_URL=http://localhost:8000
export DYNAMODB_TABLE=TESTING-LOCALLY

# 3) Create local DynamoDB Table (only exists locally for validations):
# ONLY RUN ONCE:
aws dynamodb create-table \
    --table-name TESTING-LOCALLY \
    --attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S \
    --key-schema AttributeName=PK,KeyType=HASH AttributeName=SK,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --endpoint-url http://localhost:8000 \
    --region us-east-1


# 4) Run locally the FastAPI server with uvicorn:
cd src
uvicorn todo_app.api.v1.main:app --host 0.0.0.0 --port 9999 --reload


## FINISH LOCAL TESTS:
docker-compose down
# -> Ctrl + C in the uvicorn server command
