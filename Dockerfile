# Base image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

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
    postgresql-client \
    yasm \
    libass-dev \
    libfreetype6-dev \
    libsdl2-dev \
    libtool \
    libva-dev \
    libvdpau-dev \
    libvorbis-dev \
    libxcb1-dev \
    libxcb-shm0-dev \
    libxcb-xfixes0-dev \
    pkg-config \
    texinfo \
    zlib1g-dev

# Install Rust (only for FFmpeg build, remove afterwards)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Ensure Rust is available in the following steps
ENV PATH="/root/.cargo/bin:${PATH}"

# Clone and build FFmpeg
RUN git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg && \
    cd ffmpeg && \
    ./configure --enable-gpl --enable-nonfree --enable-libass && \
    make -j4 && \
    make install && \
    cd .. && \
    rm -rf ffmpeg

# Remove Rust after FFmpeg build if not needed anymore
RUN rustup self uninstall -y

# Copy the requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# # Command to run the application using Gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "process_video.wsgi:application"]



