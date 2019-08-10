.PHONY: all build package deploy

AWS_PROFILE='manny'
S3_BUCKET='manny-aws-sam-artefacts'
all: build package deploy

build:
	sam build

package:
	sam package --s3-bucket ${S3_BUCKET}

deploy:
	sam deploy \
		--template-file packaged-header-add.yaml \
		--stack-name lambda-edge-header-add \
		--capabilities CAPABILITY_IAM
