FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY docker/pip.conf /root/.pip/pip.conf
COPY docker/requirements.txt /root/.pip/local-requirements.txt
# RUN pip install flask
RUN pip install -r /root/.pip/local-requirements.txt


RUN rm -rf /usr/src/app

COPY . /usr/src/app
EXPOSE 8080

CMD [ "python", "./server_main.py", "--config", "/config.yaml", "--host", "0.0.0.0"]
