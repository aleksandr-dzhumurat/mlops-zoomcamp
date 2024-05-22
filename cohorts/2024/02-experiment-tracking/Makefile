CURRENT_DIR = $(shell pwd)
include .env
export

prepare-dirs:
	mkdir -p ${CURRENT_DIR}/data_store/minio || true && \
    mkdir -p ${CURRENT_DIR}/data_store/mlflow || true