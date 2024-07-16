FROM apache/airflow:latest-python3.11

# Upgrade pip and setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# Install system dependencies
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up directories and permissions
RUN mkdir -p /opt/airflow/cache /opt/airflow/saved_model /app/wordclouds && \
    chown -R airflow:root /opt/airflow/cache /opt/airflow/saved_model /app/wordclouds

# Switch to the airflow user
USER airflow

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy saved models
COPY ./saved_model /opt/airflow/saved_model
