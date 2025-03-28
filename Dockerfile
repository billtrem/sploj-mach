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

# Expose port for Railway
EXPOSE 8080

# ✅ Run migrations, create superuser using environment variables, and start server
CMD bash -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && \
  echo \"from django.contrib.auth.models import User; \
  User.objects.filter(username=os.getenv('DJANGO_SUPERUSER_USERNAME')).exists() or \
  User.objects.create_superuser(username=os.getenv('DJANGO_SUPERUSER_USERNAME'), \
  email=os.getenv('DJANGO_SUPERUSER_EMAIL'), \
  password=os.getenv('DJANGO_SUPERUSER_PASSWORD'))\" \
  | python manage.py shell && \
  gunicorn splojsite.wsgi:application --bind 0.0.0.0:8080 --workers 4"
