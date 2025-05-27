# Use an official Python runtime as a parent image
FROM python:3.12.7-slim

# Add local directory and change permission.
COPY main.py /app

# Setup workdir in directory.
WORKDIR /app

# Install lib.
RUN apt-get update && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir \
    flask==3.0.3 \
    gunicorn==23.0.0

EXPOSE 5004

# Define the entrypoint script to be executed.
ENTRYPOINT ["gunicorn", "--preload", "--workers", "4", "--threads", "4", "-t", "1000", "-b", "0.0.0.0:5004", "main:app"] 