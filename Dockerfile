###############################################
# Base Image
###############################################
FROM python:3.11-slim as python-base

ARG UID
ARG GID
ENV UID_VAR=$UID
ENV GID_VAR=$GID

# Update the package list, install sudo, create a non-root user, and grant password-less sudo permissions
RUN apt update && \
    apt-get install -y sudo && \
    addgroup --gid $GID_VAR nonroot && \
    adduser --uid $UID_VAR --gid $GID_VAR --disabled-password --gecos "" nonroot && \
    echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.2  \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/app" \
    VENV_PATH="/app/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

###############################################
# Builder Image
###############################################
FROM python-base as builder-base

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    unzip \
    build-essential \
    libcurl4-openssl-dev \
    libssl-dev

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

# switch to non root user after all installation
USER nonroot

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY --chown=nonroot:nonroot pyproject.toml README.md .env ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --with dev

###############################################
# Production Image
###############################################
FROM python-base as production

RUN mkdir -p $PYSETUP_PATH/data/images
RUN chown nonroot $PYSETUP_PATH/data

USER nonroot

COPY --chown=nonroot:nonroot --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $PYSETUP_PATH
COPY --chown=nonroot:nonroot ./src ./src
COPY --chown=nonroot:nonroot ./tests ./tests

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
