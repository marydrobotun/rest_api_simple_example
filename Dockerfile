FROM python:3.8-alpine

MAINTAINER Mary Drobotun <marydrobotun@gmail.com>

WORKDIR /code/

COPY server_files/requirements.txt ./

RUN pip3.8 install --no-cache-dir -r ./requirements.txt

COPY . .

WORKDIR server_files/

CMD python3.8 server.py

