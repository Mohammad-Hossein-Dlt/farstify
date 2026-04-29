FROM python:3.14-alpine3.23

WORKDIR /app

COPY . .

RUN echo "https://mirror.arvancloud.ir/alpine/v3.23/main" > /etc/apk/repositories
RUN echo "https://mirror.arvancloud.ir/alpine/v3.23/community" >> /etc/apk/repositories
RUN apk update

RUN pip install uv
RUN uv sync --upgrade --no-cache

EXPOSE 80
CMD ["uv", "run", "fastapi", "run", "./src/main.py", "--proxy-headers", "--port", "80"]