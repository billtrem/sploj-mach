# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files before starting (optional but good)
RUN python manage.py collectstatic --noinput

# ✅ One-time admin user creation
RUN echo "from django.contrib.auth.models import User; User.objects.filter(username='sploj-office').exists() or User.objects.create_superuser('sploj-office', 'admin@sploj.com', 'Machynlleth25!')" | python manage.py shell

# Expose port for Railway
EXPOSE 8080

# Start Gunicorn server on Railway-compatible port
CMD ["gunicorn", "splojsite.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "4"]
