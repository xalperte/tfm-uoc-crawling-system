FROM python:3.6.9-slim

ARG ssh_prv_key
ARG ssh_pub_key

# DB connection information
ENV DB_USER tfm_uoc
ENV DB_PASSWORD tfm_uoc
ENV DB_HOST tfm_uoc_postgres
ENV DB_PORT 5432
ENV DB_NAME tfm_uoc

# CASSANDRA connection information
ENV CASSANDRA_DB_HOST tfm_uoc_dse
ENV CASSANDRA_DB_NAME tfm_uoc
ENV CASSANDRA_DB_USER tfm_uoc
ENV CASSANDRA_DB_PASSWORD tfm_uoc

# SOLR connection information
#ENV HAYSTACK_URL="http://tfm_uoc_dse:8983/solr"
ENV HAYSTACK_URL="http://host.docker.internal:8983/solr"

# REDIS connection information
ENV REDIS_HOST_PRIMARY tfm_uoc_redis

# CHROMIUM configuration
ENV CHROMIUM_BIN_FILE="/usr/bin/chromium"

# Install all the dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        openssh-server \
        libgdal-dev \
        libev4 \
        libev-dev \
        build-essential \
        curl \
        unzip \
        xvfb \
        tinywm \
        fonts-ipafont-gothic xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic \
        chromium

ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal

# Install Chrome WebDriver
RUN CHROMEDRIVER_VERSION="78.0.3904.105" && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

RUN mkdir /tfm_uoc_crawling_system

ADD . /tfm_uoc_crawling_system/

# Authorize SSH Host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

# Add the keys and set permissions
RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
    echo "$ssh_pub_key" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

RUN cd /tfm_uoc_crawling_system && pip install -r requirements_docs.txt || echo "ignore error"
RUN cd /tfm_uoc_crawling_system && python setup.py develop
RUN cd /tfm_uoc_crawling_system && pip install -r requirements.txt || echo "ignore error"
RUN cd /tfm_uoc_crawling_system && pip install -r requirements.base.txt || echo "ignore error"
RUN cd /tfm_uoc_crawling_system && pip install -r requirements_tests.txt || echo "ignore error"
RUN cd /tfm_uoc_crawling_system && pip install -r requirements_test.base.txt || echo "ignore error"

RUN mkdir -p /data/tfm_uoc_crawling_system/log

WORKDIR /tfm_uoc_crawling_system

VOLUME /tfm_uoc_crawling_system

EXPOSE 8000

CMD tail -f /dev/null