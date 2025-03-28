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

# Collect static files
RUN python manage.py collectstatic --noinput

# ✅ Run migrations, create superuser using environment variables, and start server
CMD bash -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && \
  python -c \"from django.contrib.auth.models import User; \
  from django.core.management import call_command; \
  from django.conf import settings; \
  username=settings.DJANGO_SUPERUSER_USERNAME; \
  email=settings.DJANGO_SUPERUSER_EMAIL; \
  password=settings.DJANGO_SUPERUSER_PASSWORD; \
  if not User.objects.filter(username=username).exists(): \
    User.objects.create_superuser(username=username, email=email, password=password)\" && \
  gunicorn splojsite.wsgi:application --bind 0.0.0.0:8080 --workers 4"
