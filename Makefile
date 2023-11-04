local:
	echo "Starting local environment with docker"
	docker-compose -f docker-compose.local.yml up --build

init:
	pip install -r requirements.txt

test:
	pytest tests

# Docker support
FILES := $(shell docker ps -aq)

down-local:
	docker stop $(FILES)
	docker rm $(FILES)

clean:
	docker system prune -f

logs-local:
	docker logs -f $(FILES)