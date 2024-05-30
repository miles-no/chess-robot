# Use the official Python image from the Docker Hub
FROM python:3.9.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Install Stockfish
RUN wget https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-ubuntu-x86-64-vnni512.tar -O /tmp/stockfish.tar && \
    tar -xvf /tmp/stockfish.tar -C /usr/local/bin/ && \
    rm /tmp/stockfish.tar

# Copy only the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "server.py"]