FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r requirements.txt

# Copy project
COPY . /app/

# Activate virtual environment and Collect static files
RUN /app/venv/bin/python manage.py collectstatic --noinput

# Run the application with the virtual environment’s Python
CMD ["/app/venv/bin/gunicorn", "artcritque.wsgi:application", "--bind", "0.0.0.0:8000"]
