FROM ghcr.io/home-assistant/aarch64-base-ubuntu:20.04

# Install build tools and Python dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    libffi-dev \
    libcap-dev \
    libtool \
    m4 \
    autoconf \
    autoconf-archive \
    automake \
    autotools-dev \
    pkg-config \
    build-essential \
    git \
    swig \
    wget \
    ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download and extract libgpiod v1.6.3
WORKDIR /build
RUN wget https://www.kernel.org/pub/software/libs/libgpiod/libgpiod-1.6.3.tar.xz && \
    tar xf libgpiod-1.6.3.tar.xz

WORKDIR /build/libgpiod-1.6.3

# Optional: patch out the kernel version check if needed
RUN sed -i '/AS_VERSION_COMPARE.*linux_version/,+3d' configure.ac

# Build and install libgpiod with Python bindings
#RUN ./autogen.sh
RUN ./configure --enable-bindings-python
RUN make
RUN make install

RUN echo "/usr/local/lib" > /etc/ld.so.conf.d/libgpiod.conf && ldconfig

# Confirm Python module is available (debug aid)
#RUN python3 -c "import gpiod; print('libgpiod Python bindings installed')"

# Copy your script and s6 run file
COPY gpio_server.py /gpio_server.py
COPY etc/services.d/gpio_server/run /etc/services.d/gpio_server/run
RUN chmod +x /etc/services.d/gpio_server/run


