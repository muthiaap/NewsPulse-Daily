FROM apache/airflow:latest-python3.11

# Update pip and setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# Install system dependencies
USER root
RUN mkdir -p /opt/airflow/cache && chown -R airflow:root /opt/airflow/cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Switch back to the airflow user
USER airflow

# Create a directory inside the container to store the model
RUN mkdir -p /opt/airflow/saved_model

# Copy the saved_model directory from the local machine to the container
# Adjust the path according to your local directory structure
COPY ./saved_model /opt/airflow/saved_model

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt