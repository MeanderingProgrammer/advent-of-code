# docker build -t advent .
# docker run --rm -it advent /bin/bash
FROM ubuntu:24.04

# settings
ARG PYTHON_VERSION="3.13"
ARG RUST_VERSION="1.87.0"
ENV DEBIAN_FRONTEND=noninteractive

# copy project directory
WORKDIR /app
COPY . .

# setup: install
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# setup: repositories
RUN add-apt-repository ppa:deadsnakes/ppa -y

# python: install
RUN apt-get update && apt-get install -y \
    python${PYTHON_VERSION}-venv \
    && rm -rf /var/lib/apt/lists/*

# python: setup
RUN python${PYTHON_VERSION} -m venv venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install -r scripts/requirements.txt

# rust: install
RUN apt-get update && apt-get install -y \
    rustup \
    && rm -rf /var/lib/apt/lists/*

# rust: setup
RUN rustup default ${RUST_VERSION}
