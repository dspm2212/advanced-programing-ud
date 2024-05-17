# syntax=docker/dockerfile:1.2

# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /backend/app

# Copy the requirements.txt file into the container at /app
COPY requirements_backend.txt /backend/app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements_backend.txt
RUN pip install uvicorn



# Copy the current directory contents into the container at /app
COPY . /backend/app

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the command to start uvicorn
CMD uvicorn Main:app --host 0.0.0.0 --port 8080 --