FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    vim \
    nano \
    htop \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory
WORKDIR /workspace

# Install Python development tools
RUN pip install --upgrade pip setuptools wheel

# Copy requirements files
COPY requirements.txt requirements-dev.txt ./

# Install dependencies
RUN pip install -r requirements.txt && \
    pip install -r requirements-dev.txt

# Create a non-root user for development
RUN useradd -m -s /bin/bash dev && \
    chown -R dev:dev /workspace
USER dev

# Set default command
CMD ["bash"]
