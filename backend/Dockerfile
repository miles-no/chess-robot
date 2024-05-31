# Select the base image according to the architecture
# Uncomment the line that corresponds to the architecture you are using

# For x86 architecture, use the following base image:
# FROM python:3.9.13-slim

# For arm architecture (like Raspberry Pi or macOS M1 chip), use the following base image:
FROM python:3.9.13-slim-buster

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
    unzip \
    tar \
    git \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Download the Certabo software
RUN wget https://www.certabo.com/wp-content/uploads/SOFTWARE/Release/Ubuntu/Certabo_Tabutronic_Ubuntu_4.5.zip

# Extract the Certabo software
RUN unzip /app/Certabo_Tabutronic_Ubuntu_4.5.zip -d /app

# Install the Certabo software
RUN dpkg -i /app/Certabo_Tabutronic_Ubuntu_4.5/Certabo_Tabutronic_Ubuntu_4.5.deb || true
RUN apt-get install -f

# Clone Stockfish and compile it
# Download and extract the precompiled Stockfish binary
RUN wget https://github.com/official-stockfish/Stockfish/releases/download/stockfish-dev-20240530-54e74919/stockfish-android-armv8.tar -O stockfish.tar && \
    tar -xf stockfish.tar && \
    mv stockfish /usr/local/bin/ && \
    chmod +x /usr/local/bin/stockfish && \
    rm stockfish.tar

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

# Install cmake separately
RUN pip install cmake

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