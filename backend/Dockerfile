# Use the official Python base image for arm64 architecture
FROM arm64v8/python:3.9.13-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV POSTGRES_USER=username
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=databasename

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql \
    wget \
    unzip \
    git \
    g++ \
    make \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Update CMake to the latest version if necessary
RUN apt-get update && apt-get install -y cmake

# Upgrade pip to the latest version
RUN /usr/local/bin/python -m pip install --upgrade pip

# Download and install the Certabo software
RUN wget -O /tmp/Certabo_Tabutronic_Ubuntu_4.5.zip https://www.certabo.com/wp-content/uploads/SOFTWARE/Release/Ubuntu/Certabo_Tabutronic_Ubuntu_4.5.zip && \
    unzip /tmp/Certabo_Tabutronic_Ubuntu_4.5.zip -d /app && \
    dpkg -i /app/Certabo_Tabutronic_Ubuntu_4.5/Certabo_Tabutronic_Ubuntu_4.5.deb || true && \
    apt-get install -f

# Clone Stockfish and compile it
RUN git clone https://github.com/official-stockfish/Stockfish.git /app/Stockfish && \
    cd /app/Stockfish/src && \
    make build ARCH=armv8 && \
    cp stockfish /usr/local/bin/ && \
    chmod +x /usr/local/bin/stockfish && \
    cd /app && \
    rm -rf /app/Stockfish

# Start PostgreSQL service and setup database
USER postgres
RUN service postgresql start && \
    psql -c "CREATE ROLE $POSTGRES_USER WITH LOGIN PASSWORD '$POSTGRES_PASSWORD'; ALTER ROLE $POSTGRES_USER CREATEDB;" && \
    service postgresql stop

RUN service postgresql start && \
    psql -c "CREATE DATABASE $POSTGRES_DB;" && \
    psql -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;" && \
    service postgresql stop

USER root

# Copy only the requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the start script and the rest of the application code
COPY start.sh /app/
COPY . /app/

# Give execute permissions to the start script
RUN chmod +x /app/start.sh

# Expose the port the app runs on
EXPOSE 5000

# Command to run the start script
CMD ["/app/start.sh"]
