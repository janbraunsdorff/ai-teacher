FROM python:3.9

WORKDIR /

RUN apt-get -y update && \
    apt-get -y install libpoppler-dev

ADD ./content/demo/import_data /demo_data/

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD requirements-dev.txt /requirements-dev.txt
RUN pip install -r /requirements-dev.txt

ADD start-dev-server.sh /start-dev-server.sh
RUN chmod 777 start-dev-server.sh

WORKDIR /backend

ENTRYPOINT /start-dev-server.sh