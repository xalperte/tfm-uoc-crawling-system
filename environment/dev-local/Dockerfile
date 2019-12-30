FROM xalperte/base-davinci:0.1

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

RUN mkdir /tfm_uoc_crawling_system

ADD . /tfm_uoc_crawling_system/

RUN pip install Cython django-haystack

RUN cd /tfm_uoc_crawling_system \
    && python setup.py develop \
    && pip install django_caravaggio_rest_api[spatial] \
    && pip install -r requirements_test.base.txt || echo "ignore error"

RUN mkdir -p /data/tfm_uoc_crawling_system/log

WORKDIR /tfm_uoc_crawling_system

VOLUME /tfm_uoc_crawling_system

EXPOSE 8000

CMD tail -f /dev/null