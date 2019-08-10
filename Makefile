.PHONY: all test build package deploy

AWS_PROFILE='manny'
FUNCTION_NAME='HeaderAddFunction'
S3_BUCKET='manny-aws-sam-artefacts'
all: build run test package deploy

build:
	sam build
run:
	sam local invoke ${FUNCTION_NAME} --event event.json

test:
	python3 -m pytest tests/ -v

package:
	sam package --s3-bucket ${S3_BUCKET}

deploy:
	sam deploy \
		--template-file packaged-header-add.yaml \
		--stack-name lambda-edge-header-add \
		--capabilities CAPABILITY_IAM
