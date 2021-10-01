FROM iconloop/goloop:0.9.4 as base

ARG SERVICE_NAME
ENV SERVICE_NAME ${SERVICE_NAME:-api}

# GO ENV VARS
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/opt:${PYTHONPATH}"

WORKDIR /opt

RUN apk --update --no-cache \
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
    build-base \
    linux-headers \
    cmake \
    bash \
    perl \
    zlib-dev \
    bzip2-dev \
    snappy-dev \
    lz4-dev \
    zstd-dev \
    libtbb-dev \
    gflags-dev \
  && apt-get clean && \
    pip install --upgrade pip

ARG ROCKSDB_VERSION
LABEL ROCKSDB_VERSION="$ROCKSDB_VERSION"
RUN cd /work && \
    git clone https://github.com/facebook/rocksdb.git && \
    cd rocksdb && \
    git checkout ${ROCKSDB_VERSION} && \
    PORTABLE=1 make shared_lib

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
