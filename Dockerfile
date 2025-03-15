# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Add /app to PYTHONPATH
ENV PYTHONPATH=/app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install netcat (nc) to wait for MySQL availability
RUN apt-get update && apt-get install -y netcat-traditional

# Copy the rest of the application code including entrypoint.sh
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Expose the port FastAPI will run on
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
