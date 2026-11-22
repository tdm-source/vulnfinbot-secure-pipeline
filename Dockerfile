
FROM python:3.12-slim

WORKDIR /app

# Update Debian system packages
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies and upgrade vulnerable setuptools
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m pip install --no-cache-dir --upgrade "setuptools>=78.1.1" \
    && python -m pip check

# Copy application source code
COPY app/ ./app/
COPY run.py .

# Run as a non-root user
RUN useradd --create-home appuser
USER appuser

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
