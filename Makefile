.PHONY: all test build package deploy

AWS_PROFILE='manny'
FUNCTION_NAME='HeaderAddFunction'
S3_BUCKET='manny-aws-sam-artefacts'
all: test build package deploy

test:
	sam local invoke ${FUNCTION_NAME} --event event.json

build:
	sam build

package:
	sam package --s3-bucket ${S3_BUCKET}

deploy:
	sam deploy \
		--template-file packaged-header-add.yaml \
		--stack-name lambda-edge-header-add \
		--capabilities CAPABILITY_IAM
