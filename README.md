
## Description
* Image Retreival Application that recommends clothes based on user's inputs.
* Uses FashionClip to map input image/text into the same latent space as the repository of image vectors.
* Uses cosine similarity to find the top n most similar clothes based on inputs.


### Build Environment for testing
```bash
python3 -m venv .venv
python3 -m pip install --upgrade pip
source .venv/bin/activate
pip install poetry
poetry install --with dev
pre-commit instal
```

### Linting and Tests
```bash
pytest --cov-report term-missing --cov=src tests/
pre-commit run --all-files
```

### Run app
```bash
docker compose up
```
