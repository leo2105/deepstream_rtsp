FROM debian:10-slim
RUN apt-get update && \
      DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends curl ca-certificates gstreamer-1.0 gstreamer1.0-rtsp gstreamer1.0-plugins-ugly gstreamer1.0-tools ffmpeg \
      && mkdir /app && cd /app && curl -L https://github.com/aler9/rtsp-simple-server/releases/download/v0.15.5/rtsp-simple-server_v0.15.5_linux_amd64.tar.gz -o rtsp-simple-server.tar.gz \
      && tar -xvf rtsp-simple-server.tar.gz && rm rtsp-simple-server.tar.gz \
      && apt-get clean \
      && apt-get autoclean \
      && apt-get -y autoremove \
      && rm -rf /tmp/* /var/tmp/* \
      && rm -rf /var/lib/apt/lists/* \
      && rm -f /var/cache/apt/archives/*.deb \
      && rm -f /var/cache/apt/archives/partial/*.deb \
      && rm -f /var/cache/apt/*.bin \
      && rm -rf /root/.[acpw]*
#      && apt-get install -y vlc

#RUN useradd -m vlcuser

COPY ./rtsp-simple-server_ffmpeg.yml /app/rtsp-simple-server.yml

WORKDIR /app
EXPOSE 8000
EXPOSE 8001
EXPOSE 8554
#ENTRYPOINT /app/rtsp-simple-server
