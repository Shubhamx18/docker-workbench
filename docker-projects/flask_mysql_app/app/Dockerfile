# 1. Use lightweight Python image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Install system dependencies (needed for MySQL + performance)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements first (for caching)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy all project files
COPY . .

# 7. Expose port
EXPOSE 5000

# 8. Environment variables
ENV PYTHONUNBUFFERED=1

# 9. Run app using production server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]