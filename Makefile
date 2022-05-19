CURRENT_DIR = $(shell pwd)
USER_NAME = $(shell whoami)
USER_ID = $(shell id -u)
USER_GROUP = $(shell id -g)

build:
	docker build \
		--build-arg USER_ID="${USER_ID}" \
		--build-arg GROUP_ID="${GROUP_ID})" \
		-f ${CURRENT_DIR}/Dockerfile \
		-t mlops-homework-${USER_NAME}:dev \
		${CURRENT_DIR}

clear:
	docker rm -f ${USER_NAME}_notebook || true

run-jupyter: clear
	sudo docker run -it -d --rm \
	    -p 8888:8888 \
	    -v ${CURRENT_DIR}/01-intro:/srv/experiments \
	    --name ${USER_NAME}_notebook \
	    mlops-homework-${USER_NAME}:dev \
		"jupyter" notebook experiments --ip 0.0.0.0 --port 8888 --NotebookApp.token='' --NotebookApp.password='' --allow-root --no-browser 