FROM node:slim

USER 0
RUN mkdir /app
WORKDIR /app

RUN npm install -g @angular/cli

ADD . /app
RUN npm install

ENV NODE_OPTIONS=--openssl-legacy-provider
CMD ls -al && ng serve --host 0.0.0.0
