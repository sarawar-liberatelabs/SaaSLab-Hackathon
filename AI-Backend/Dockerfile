FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Add build argument for port
ARG PORT=8000
ENV PORT=${PORT}

# Install required system packages (for psycopg and compiling)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install packages
COPY requirements.txt .

# Use psycopg with binary build to avoid manual compilation
RUN pip install --no-cache-dir "psycopg[binary]" && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code into the container
COPY . .

# Expose the port
EXPOSE ${PORT}

# Default command can be overridden by docker-compose
CMD ["python", "-m", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=${PORT}"]
