run: ## App start
	export PYTHONPATH=$$PWD && \
	uv run src/main.py

run_celery: ## Celery start
	 uv run celery --app=src.tasks.celery_app:celery_app worker -l INFO

run_celery_beat: ## Celery start
	 uv run celery --app=src.tasks.celery_app:celery_app worker -l INFO -B

run_hw: ## Hw start
	uv run hw/redis_cache_decorator.py

prepare: ## Linter for all files
	uv run pre-commit run --all-files

run-tests: ## Run pytest
	pytest -v

build: ## docker build
	docker build -t booking .

docker-run-rm: ## run container with rm after
	docker run --rm --env-file .env -p 8000:8000 --name booking-api booking
