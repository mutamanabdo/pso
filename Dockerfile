# Use an official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose the port your app runs on (e.g., 80)
EXPOSE 80

# Command to run the app (matches your Procfile)
CMD ["gunicorn", "pso.wsgi:application", "--bind", "0.0.0.0:80"]
