
# IMAGE SEARCH APP

[![CI](https://github.com/teoshuqi/image-search/actions/workflows/main.yml/badge.svg)](https://github.com/teoshuqi/image-search/actions/workflows/main.yml)
[![CodeQL](https://github.com/teoshuqi/image-search/actions/workflows/codeql.yml/badge.svg)](https://github.com/teoshuqi/image-search/actions/workflows/codeql.yml)


## Description
* Image Retreival Application that recommends clothes based on user's inputs.
* Uses FashionClip to map input image/text into the same latent space as the repository of image vectors.
* Uses cosine similarity to find the top n most similar clothes based on inputs.


### Build Environment for testing
```bash
python3 -m venv .venv
python3 -m pip install --upgrade pips
source .venv/bin/activate
pip install poetry
poetry install --with dev
pre-commit install
```

### Linting and tests
```bash
make precommit
make lint
make up
make test
```

### Run app
```bash
make up
```

### Test

### API methods ###
* GET /healthcheck
* POST /update/{pages: int}
* POST /search
    * {text:"", type:"text"}
