.PHONY: all requirements lint test static_analysis build coverage

all: requirements lint test static_analysis build

requirements:
	poetry install --with dev

lint:
	echo "Running code style checks..."
	black src/ tests/ --check; isort src/ tests/ --check --diff; flake8 src/ tests/; bandit -c pyproject.toml -r src/ tests/

test:
	pytest --cov-report term-missing --cov=src tests/

coverage:
	echo "to add coverage code"	

up:
	docker compose up

down: 
	docker compose down

prune:
	docker system prune -a

clean:
	echo "to add clean up code"
