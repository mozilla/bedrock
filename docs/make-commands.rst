help: you're reading it
gulp: run gulp in a bedrock_dev container
js-lint: run 'gulp js:lint' in a bedrock_dev container
unit: run the unit tests in a bedrock_dev container
headless: run the headless integration tests in a bedrock_dev container
test: run both the unit tests and the headless integration tests in a bedrock_dev container
devserver: run the django development server in a bedrock_dev docker image
codeserver: run gunicorn in a bedrock_code docker container
stop: stop all docker containers
shell_plus: run the shell_plus management command from django_extensions in a bedrock_dev container
collectstatic: run the collectstatic management command in a bedrock_dev container
bash: run a bash shell in a bedrock_dev container
build-base: build a bedrock_base image
build-squash-base: build a bedrock_base image and use docker-squash to reduce the size
build-dev: build a bedrock_dev image 
build-code: build a bedrock_code image on top of the bedrock_base image with the same tag
build-l10n: build a bedrock_l10n image on top of the bedrock_code image with the same tag
push-euw: push to the euw deis cluster. assumes a private registry listening on port 5000
push-usw: push to the usw deis cluster. assumes a private registry listening on port 5001
media-change: requires MEDIA_PATH arg. copies file to static dir and if it's a js file runs 'make js-lint'
fswatch-media: watch media directory with fswatch and call 'make media-change' for each changed file
