FROM python:3.10-slim

# podstawowe pakiety + dependencies dla pygame, Xvfb, VNC i numpy
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libportmidi-dev libavformat-dev libavcodec-dev libavutil-dev libswscale-dev \
    libjpeg-dev libfreetype6-dev pulseaudio \
    xvfb x11vnc fluxbox wget net-tools x11-utils \
    python3-numpy \
 && rm -rf /var/lib/apt/lists/*

# pobierz noVNC + websockify (tworzymy katalog docelowy przed tar)
RUN mkdir -p /opt/novnc && \
    wget -qO- https://github.com/novnc/noVNC/archive/refs/heads/master.tar.gz | tar xz --strip-components=1 -C /opt/novnc && \
    mkdir -p /opt/novnc/utils/websockify && \
    wget -qO- https://github.com/novnc/websockify/archive/refs/heads/master.tar.gz | tar xz --strip-components=1 -C /opt/novnc/utils/websockify

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app

ENV XDG_RUNTIME_DIR=/tmp/xdg
ENV SDL_AUDIODRIVER=dummy
ENV PYGAME_HIDE_SUPPORT_PROMPT=1

EXPOSE 5901 6901

CMD /bin/bash -c "\
  mkdir -p $XDG_RUNTIME_DIR && chmod 1777 $XDG_RUNTIME_DIR; \
  Xvfb :1 -screen 0 600x850x24 & \
  export DISPLAY=:1; \
  fluxbox & \
  sleep 0.5; \
  x11vnc -display :1 -nopw -forever -shared -rfbport 5901 -noxdamage & \
  /opt/novnc/utils/websockify/run --web=/opt/novnc 6901 localhost:5901 & \
  sleep 1; \
  python main.py"
