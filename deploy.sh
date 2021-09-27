#!/bin/sh

STACK_NAME="cetac-apis"
S3_BUCKET="cetac-apis-package"

sam build

sam package \
--s3-bucket $S3_BUCKET

sam deploy \
--stack-name $STACK_NAME \
--s3-bucket $S3_BUCKET \
--capabilities CAPABILITY_NAMED_IAM