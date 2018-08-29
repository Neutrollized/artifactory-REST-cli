FROM python:2-alpine3.7


RUN apk add --no-cache automake autoconf libtool python-dev g++ make \
    && pip install --upgrade pip setuptools \
    && pip install jq requests

COPY artifactory-REST-cli.pyc /usr/local/bin/.

WORKDIR /mnt

ENTRYPOINT ["python", "/usr/local/bin/artifactory-REST-cli.pyc"]
