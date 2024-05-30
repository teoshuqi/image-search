.PHONY: all requirements lint test static_analysis build coverage

all: requirements lint test static_analysis build

dev_requirements:
	poetry install --with dev

requirements:
	poetry install --no-dev

lint:
	echo "Running code style checks..."
	black src/ tests/ --check; isort src/ tests/ --check --diff; flake8 src/ tests/; bandit -c pyproject.toml -r src/ tests/

test:
	poetry run pytest --cov-report term-missing --cov=src tests/  # Run integration tests

coverage:
	echo "to add coverage code"

up:
	docker compose up -d

down:
	docker compose down

prune:
	docker system prune -a

clean:
	echo "to add clean up code"
