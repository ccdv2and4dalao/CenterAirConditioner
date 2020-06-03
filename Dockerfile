FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY docker/pip.conf /root/.pip/pip.conf

RUN pip install flask
RUN rm -rf /usr/src/app

COPY . /usr/src/app
EXPOSE 8080

CMD [ "python", "./main.py", "--config", "/config.yaml"]
