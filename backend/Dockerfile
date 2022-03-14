FROM python:3.9

WORKDIR /

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD requirements-dev.txt /requirements-dev.txt
RUN pip install -r /requirements-dev.txt

ADD start-dev-server.sh /start-dev-server.sh
RUN chmod 777 start-dev-server.sh

WORKDIR /backend

ENTRYPOINT /start-dev-server.sh