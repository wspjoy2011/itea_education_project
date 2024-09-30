FROM python:3.10

# Set working directory
WORKDIR /usr/src/app

# Environment settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR off
ENV PYTHONPATH /

# Install necessery packages
RUN apt update && apt install -y gcc libpq-dev netcat-openbsd coreutils

# Copy and install dependancies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy source code
COPY . .

# Copy and configure entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

