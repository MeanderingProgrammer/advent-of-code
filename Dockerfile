FROM ubuntu:24.04

# copy working directory
COPY . /advent
WORKDIR /advent

# basic setup
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# python
RUN add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update && apt-get install -y \
    python3.13-venv \
    && rm -rf /var/lib/apt/lists/*

# python environment
RUN python3.13 -m venv venv
ENV PATH="/advent/venv/bin:$PATH"
RUN pip install -r scripts/requirements.txt

# rust
RUN apt-get update && apt-get install -y \
    rustup \
    && rm -rf /var/lib/apt/lists/*

# rust environment
RUN rustup toolchain install 1.87.0 && rustup default 1.87.0
