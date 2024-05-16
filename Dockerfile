# Use the official Python image as a base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of your Django project
COPY . .

# Expose the port that your Django application will run on
EXPOSE 8000

# Specify the command to run your Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
