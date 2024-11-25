FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install -y ffmpeg

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD uvicorn main:app --reload --port 8000 --host 0.0.0.0