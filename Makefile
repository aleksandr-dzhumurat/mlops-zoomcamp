CURRENT_DIR = $(shell pwd)
USER_NAME = $(shell whoami)
USER_ID = $(shell id -u)
USER_GROUP = $(shell id -g)s

prepare-dirs:
	mkdir -p ${CURRENT_DIR}/data || true

build: prepare-dirs
	docker build \
		--build-arg USER_ID="${USER_ID}" \
		--build-arg GROUP_ID="${GROUP_ID}" \
		-f ${CURRENT_DIR}/Dockerfile \
		-t mlops-homework-${USER_NAME}:dev \
		${CURRENT_DIR}

clear:
	docker rm -f ${USER_NAME}_notebook || true

run-jupyter: clear
	docker run -it -d --rm \
	    -p 8888:8888 \
	    -v ${CURRENT_DIR}/:/srv/experiments \
	    -v /Users/username/Downloads/data:/srv/data \
	    --name mlops_notebook \
	    mlops-homework-${USER_NAME}:dev \
		"jupyter" notebook experiments --ip 0.0.0.0 --port 8888 --NotebookApp.token='' --NotebookApp.password='' --allow-root --no-browser 

stop:
	docker rm -f mlops_notebook || true