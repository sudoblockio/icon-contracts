#FROM python:3.9-slim-buster as base
FROM golang:1.16.8-bullseye as base

ARG SERVICE_NAME
ENV SERVICE_NAME ${SERVICE_NAME:-api}

# GO ENV VARS
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/opt:${PYTHONPATH}"

WORKDIR /opt

RUN apt-get update
RUN apt-get -y --no-install-recommends install \
    gcc \
    g++ \
    xxd \
    unzip \
    netcat \
    net-tools \
    librocksdb-dev \
    software-properties-common \
    python3-dev \
    python3-pip \
    git \
    libsecp256k1-dev \
    python3-setuptools \
  && apt-get clean && \
    pip install --upgrade pip

RUN git clone https://github.com/icon-project/goloop goloop && \
    cd goloop && \
    pip install -r pyee/requirements.txt && \
    make && \
    make pyexec && \
    apt uninstall git -y

ENV PATH="/opt/goloop/bin:${PATH}"

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY icon_contracts ./icon_contracts

FROM base as test

FROM base as prod
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh
ENTRYPOINT ./entrypoint.sh $SERVICE_NAME
