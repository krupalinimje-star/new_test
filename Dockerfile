# Use an official lightweight Python base image
FROM python:3.12-slim

# Set environment variables to optimize Python runtime in containers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for package compilation and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Expose port 8000 for the Django application
EXPOSE 8000

# Run migrations, seed mock data, and launch the development server
CMD ["sh", "-c", "if [ -n \"$DB_HOST\" ]; then python -c \"import socket, time, os; s = socket.socket(); s.settimeout(1); host = os.environ.get('DB_HOST'); port = int(os.environ.get('DB_PORT', 5432)); \nwhile True:\n    try:\n        s.connect((host, port)); break\n    except:\n        print(f'Waiting for database {host}:{port}...'); time.sleep(1)\"; fi && python manage.py migrate && python populate_data.py && python manage.py runserver 0.0.0.0:8000"]

