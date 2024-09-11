# # Base image
# FROM python:3.12

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set work directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt /app/
# RUN pip install --upgrade pip && pip install -r requirements.txt

# # # Install dependencies and multiarch support
# # RUN dpkg --add-architecture i386 && \
# #     apt-get update && \
# #     apt-get install -y wine32:i386

# # # Install redis-tools (for Debian-based images)
# # RUN apt-get update && apt-get install -y redis-tools

# # # Install wine (for running Windows binaries on Linux)
# # RUN apt-get install -y wine

# # # Add these lines after installing Wine
# # RUN mkdir -p /root/.wine
# # RUN winecfg

# # # Copy CCExtractor files into the Docker image
# # COPY ccextractor /usr/local/bin/CCExtractor

# # # Make the ccextractor.exe executable
# # RUN chmod +x /usr/local/bin/CCExtractor/ccextractor.exe

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     git \
#     build-essential \
#     cmake \
#     libglfw3-dev \
#     libglew-dev \
#     libtesseract-dev \
#     libleptonica-dev \
#     libcurl4-openssl-dev \
#     libavformat-dev \
#     libavcodec-dev \
#     libswscale-dev \
#     tesseract-ocr \
#     libtesseract-dev \
#     libleptonica-dev

# # Clone and build CCExtractor
# RUN git clone https://github.com/CCExtractor/ccextractor.git && \
#     cd ccextractor/linux && \
#     ./build

# # Move the ccextractor binary to /usr/local/bin
# RUN mv /app/ccextractor/linux/ccextractor /usr/local/bin/

# # Clean up
# RUN rm -rf /app/ccextractor

# # Copy the rest of the project files
# COPY . /app/


# Base image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Increase git buffer size to handle large data transfers
RUN git config --global http.postBuffer 524288000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    libglfw3-dev \
    libglew-dev \
    libtesseract-dev \
    libleptonica-dev \
    libcurl4-openssl-dev \
    libavformat-dev \
    libavcodec-dev \
    libswscale-dev \
    tesseract-ocr \
    curl \
    gnupg \
    autoconf \
    clang \
    libclang-dev \
    gpac  # Install gpac

# Install Rust and Cargo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && export PATH="$PATH:/root/.cargo/bin"

# Shallow clone CCExtractor repository to reduce data transfer
RUN git clone --depth 1 https://github.com/CCExtractor/ccextractor.git

# Build CCExtractor using CMake
RUN cd ccextractor \
    && mkdir build \
    && cd build \
    && cmake ../src/ -DWITH_OCR=ON \
    && make \
    && make install

# Clean up the repository after building
RUN rm -rf /app/ccextractor

# Copy the rest of the project files
COPY . /app/

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt


