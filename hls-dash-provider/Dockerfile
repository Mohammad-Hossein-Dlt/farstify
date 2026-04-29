FROM python:3.14-alpine3.23

WORKDIR /app

COPY . .

RUN echo "https://mirror.arvancloud.ir/alpine/v3.23/main" > /etc/apk/repositories
RUN echo "https://mirror.arvancloud.ir/alpine/v3.23/community" >> /etc/apk/repositories
RUN apk update
RUN apk add --no-cache ffmpeg

# RUN echo "deb http://mirror-linux.runflare.com/debian trixie main" > /etc/apt/sources.list
# RUN echo "deb http://mirror-linux.runflare.com/debian-security trixie-security main" > /etc/apt/sources.list
# RUN apt-get update 
# RUN apt-get -y install -y ffmpeg
# RUN rm -rf /var/lib/apt/lists/*

RUN pip install uv
RUN uv sync --upgrade --no-cache

EXPOSE 80
CMD ["uv", "run", "faststream", "run", "src.main:app"]