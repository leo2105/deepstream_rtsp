FROM nvcr.io/nvidia/deepstream:5.1-21.02-devel

# install dependencies
RUN apt-get update && \
    apt-get install -y python-gi-dev python3-gst-1.0 autoconf libtool python3-pip python3-dev graphviz

# install gst-python
WORKDIR /opt/
RUN export GIT_SSL_NO_VERIFY=1 && export GST_LIBS="-lgstreamer-1.0 -lgobject-2.0 -lglib-2.0" && \
    export GST_CFLAGS="-pthread -I/usr/include/gstreamer-1.0 -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include" && \
    git clone https://github.com/GStreamer/gst-python.git && cd gst-python && git checkout 1a8f48a && \
    ./autogen.sh --disable-gtk-doc --noconfigure PYTHON=python3 && \
    ./configure --prefix=/usr --with-libpython-dir=/usr/lib/x86_64-linux-gnu PYTHON=python3 && \
    make && make install

# install DeepStream python bindings
RUN cd /opt/nvidia/deepstream/deepstream/lib/ && python3 setup.py install

# install python dependencies
RUN python3 -m pip install --upgrade pip && \ 
    python3 -m pip install kafka pyyaml pybind11 numpy influxdb opencv-python imagehash watchdog gpustat

ENV RUSTUP_HOME=/rust
ENV CARGO_HOME=/cargo 
ENV PATH=/cargo/bin:/rust/bin:$PATH

RUN apt-get install -y curl && (curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain nightly --no-modify-path) && rustup default nightly

RUN apt-get install -y vlc
RUN useradd -m vlcuser
