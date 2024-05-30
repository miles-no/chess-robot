# Use the official Python image from the Docker Hub
FROM python:3.9.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV POSTGRES_USER=username
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=databasename

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql \
    wget \
    tar \
    git \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Check the architecture
RUN uname -m

# Clone Stockfish and compile it
RUN git clone https://github.com/official-stockfish/Stockfish.git && \
    cd Stockfish/src && \
    make build ARCH=armv8 && \
    cp stockfish /usr/local/bin/ && \
    chmod +x /usr/local/bin/stockfish && \
    cd ../.. && \
    rm -rf Stockfish

# Start PostgreSQL service and setup database
USER postgres
RUN service postgresql start && \
    psql -c "CREATE ROLE $POSTGRES_USER WITH LOGIN PASSWORD '$POSTGRES_PASSWORD'; ALTER ROLE $POSTGRES_USER CREATEDB;"

RUN service postgresql start && \
    psql -c "CREATE DATABASE $POSTGRES_DB;" && \
    psql -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;"

USER root

# Copy only the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the start script and the rest of the application code
COPY start.sh .
COPY . .

# Give execute permissions to the start script
RUN chmod +x start.sh

# Expose the port the app runs on
EXPOSE 5000

# Command to run the start script
CMD ["./start.sh"]