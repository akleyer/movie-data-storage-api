# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install only the requirements first to leverage Docker layer caching
COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application folder
COPY app/ ./app

# Copy the Flask application entry point
COPY app.py .

# Use gunicorn to serve the Flask application
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
