FROM python:2-alpine3.7

WORKDIR /tmp

COPY requirements.txt .
COPY artifactory-REST-cli.py .

RUN apk add --no-cache automake autoconf libtool python-dev g++ make \
    && pip install --upgrade pip setuptools \
    && pip install -r requirements.txt \
    && python -m compileall artifactory-REST-cli.py \
    && cp artifactory-REST-cli.pyc /usr/local/bin/.

WORKDIR /mnt

ENTRYPOINT ["python", "/usr/local/bin/artifactory-REST-cli.pyc"]
