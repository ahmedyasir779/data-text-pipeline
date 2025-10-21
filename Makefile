# Makefile for Docker operations

.PHONY: build run test clean help

# Variables
IMAGE_NAME = data-text-pipeline
IMAGE_TAG = latest
CONTAINER_NAME = dtp-container

help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker image"
	@echo "  make run      - Run container with sample data"
	@echo "  make test     - Run tests in container"
	@echo "  make shell    - Open shell in container"
	@echo "  make clean    - Remove image and containers"

build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

run:
	@echo "Running pipeline..."
	docker run --rm \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/output:/app/output \
		$(IMAGE_NAME):$(IMAGE_TAG) \
		python cli.py --data-file /app/data/customer_reviews.csv --text-column review --all

test:
	@echo "Running tests..."
	docker run --rm \
		$(IMAGE_NAME):$(IMAGE_TAG) \
		pytest tests/ -v

shell:
	@echo "Opening shell..."
	docker run -it --rm \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/output:/app/output \
		$(IMAGE_NAME):$(IMAGE_TAG) \
		/bin/bash

clean:
	@echo "Cleaning up..."
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG)
	docker system prune -f

push:
	@echo "Pushing to Docker Hub..."
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) YOUR_DOCKERHUB_USERNAME/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push YOUR_DOCKERHUB_USERNAME/$(IMAGE_NAME):$(IMAGE_TAG)