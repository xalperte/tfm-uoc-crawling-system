Django DaVinci Crawler project template
=======================================

This is a simple DaVinci Crawling project template with the preferred
setup.

We can use this project template to implement crawlers or to setup a
project with multiple crawlers all together in the same RESTful API.

This template has also support for Docker and is also optimized for
Google App Engine deployments.

Features
--------

-  `Caravaggio REST API
   Framework <https://github.com/buildgroupai/django-caravaggio-rest-api>`__
   (Django 2.0+, DRF, DataStax/Cassandra)
-  `DaVinci Crawling
   Framwework <https://github.com/buildgroupai/django-davinci-crawling>`__
-  PostgreSQL database support with psycopg2.
-  DataStax database support with DSE Driver
-  Get value insight and debug information while on Development with
   django-debug-toolbar.
-  Collection of custom extensions with django-extensions.
-  HTTPS and other security related settings on Staging and Production.
-  Docker image
-  Google App Engine deployment support (custom environment)

Environment Setup
-----------------

We need to prepare the environment to install and execute the crawler.

We need to install, configure and start the following services:

-  DataStax Enterprise 6.x
-  PostgreSQL 9.6
-  Redis 3

To do that we can follow the instructions
`here <https://github.com/buildgroupai/django-caravaggio-rest-api/blob/master/docs/local_environment.md>`__.

Once the previous services are ready, we can proceed with the
installation.

How to create a new project
---------------------------

Follow the next instructions to create a new crawling project with one
crawler:

::

    $ conda create -n myproject pip python=3.6
    $ conda activate myproject

    $ pip install django>=2

    $ conda install -y gdal

    $ django-admin.py startproject \
      --template=https://github.com/buildgroupai/davinci-crawling-project-template/archive/develop.zip \
      --name=Dockerfile \
      --name=Makefile \
      --extension=py,md,env,sh,template,yamltemplate,ini,conf,json,cfg,rst,Dockerfile \
      myproject

    $ cd myproject/src

    $ python manage.py startapp \
       --template=https://github.com/buildgroupai/davinci-crawling-app-template/archive/develop.zip \
       --extension=py,md,env,sh,template,yamltemplate,ini,conf,json,rst,Dockerfile \
       mycrawler

    # Returns to your project folder
    $ cd ..

    $ python setup.py develop
    $ pip install django_davinci_crawling[spatial]
    $ pip install -r requirements_test.base.txt
    $ sudo mkdir -p /data/crawler_one/log
    $ sudo chown -R `whoami`:staff /data/crawler_one

**NOTE**: by default we are using the ``dse-driver`` to connect to
cassandra or DataStax Enterprise. If you want to use
``cassandra-driver`` edit ``setup.py`` and change the dependency.

**NOTE**: the installation of the dependencies will take some time
because the ``dse-driver`` or ``cassandra-driver`` has to be compiled.

We can add as many crawlers as we want.

Test crawler
~~~~~~~~~~~~

To test the crawler we will need to:

-  Add the crawler app to the list of INSTALLED\_APPS;
-  Add some logging configuration on the settings.py;
-  Add the statics files to the settings.py;
-  Add the crawler urls to the project urls.

If you want to test the Bovespa crawler too that comes with
``davinci-crawling``, you should edit the
``settings.py file and add davinci_crawling.example.bovespa`` to the
list of ``INSTALLED_APPS``, just after the ``davinci_crawling``
application.

.. code-block:: python

    # Application definition
    INSTALLED_APPS = [
        ...
        'davinci_crawling',
        'davinci_crawling.example.bovespa',
    ]

    INSTALLED_APPS += [
        'myproject',
        'mycrawler'
    ]

Add now the logging configuration on the ``settings.py`` too.

.. code-block:: python

    'davinci_crawler_crawler_11': {
        'handlers': ['console', 'mail_admins'],
        'level': 'DEBUG',
        'propagate': True,
    },

The last thing you need to do on ``settings.py`` is add the crawler staticfiles
to the staticfiles on the project.

.. code-block:: python
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        os.path.join(BASE_DIR + '/crawler_one/static'),

        # Your crawler static files go here
        os.path.join(BASE_DIR + '/crawler_11/static'),
        os.path.join(BASE_DIR + '/crawler_12/static'),
    )

And now we can update the ``myproject.urls.py`` file as shown here:

.. code-block:: python

    from mycrawler.api.urls import urlpatterns as mycrawler_urls

    ....

    urlpatterns = [
        ...
        ...

        url(r'^api-schema/mycrawler/$',
            get_schema_view(title="Mycrawler API",
                            patterns=[url(r'^mycrawler/',
                                          include(mycrawler_urls))])),

        # Mycrawler API version
        url(r'^mycrawler/', include(mycrawler_urls)),
    ]

Setup the databases
~~~~~~~~~~~~~~~~~~~

Follow the instructions
`here <https://github.com/buildgroupai/django-caravaggio-rest-api/blob/master/docs/local_environment.md>`__
to prepare your backend for development.

In this step we are going to populate the databases and its tables. The
default database is a PostgreSQL (you can change it) and then we also
have the cassandra database, that can be a Cassandra or DSE server.

You can change the SQL server editing the dependencies in the
``setup.py`` and changing the ``psycopg2-binary`` library by the one
that contains the drivers to connect to your backend. You should
configure the connection in the ``DATABASES`` parameter of the
``settings.py`` of the project.

Once the database services are ready, we can populate the database and
its tables running the following instruction:

::

    $ python manage.py migrate

    Operations to perform:
      Apply all migrations: admin, auth, authtoken, contenttypes, sites
    Running migrations:
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying admin.0003_logentry_add_action_flag_choices... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying auth.0007_alter_validators_add_error_messages... OK
      Applying auth.0008_alter_user_username_max_length... OK
      Applying auth.0009_alter_user_last_name_max_length... OK
      Applying authtoken.0001_initial... OK
      Applying authtoken.0002_auto_20160226_1747... OK
      Applying sites.0001_initial... OK
      Applying sites.0002_alter_domain_unique... OK

Populate the DataStax Enterprise (DSE) or Cassandra database:

::

    $ python manage.py sync_cassandra

    Creating keyspace myproject [CONNECTION cassandra] ..
    Syncing django_cassandra_engine.sessions.models.Session
    Syncing davinci_crawling.models.Checkpoint
    Syncing myproject.models.MyprojectResource

Populate the DataStax Enterprise (DSE) search indexes. This feature is
only available for a DSE configuration:

::

    $ python manage.py sync_indexes

    INFO Creating indexes in myproject4 [CONNECTION cassandra] ..
    INFO Creating index %s.%s
    INFO Index class associated to te model myproject.models.MyprojectResourceIndex
    INFO Creating SEARCH INDEX if not exists for model: <class 'django_cassandra_engine.models.MyprojectResource'>
    INFO Setting index parameters: realtime = true
    INFO Setting index parameters: autoCommitTime = 100
    INFO Setting index parameters: ramBufferSize = 2048
    INFO Processing field field <class 'haystack.fields.CharField'>(situation)
    WARNING Maybe te field has been already defined in the schema. Cause: Error from server: code=2200 [Invalid query] message="The search index schema is not valid because: Can't load schema schema.xml: [schema.xml] Duplicate field definition for 'situation' [[[situation{type=StrField,properties=indexed,omitNorms,omitTermFreqAndPositions}]]] and [[[situation{type=StrField,properties=indexed,stored,omitNorms,omitTermFreqAndPositions}]]]"
    INFO Processing field field <class 'haystack.fields.CharField'>(name)
    WARNING Maybe te field has been already defined in the schema. Cause: Error from server: code=2200 [Invalid query] message="The search index schema is not valid because: Can't load schema schema.xml: [schema.xml] Duplicate field definition for 'name' [[[name{type=StrField,properties=indexed,omitNorms,omitTermFreqAndPositions}]]] and [[[name{type=StrField,properties=indexed,stored,omitNorms,omitTermFreqAndPositions}]]]"
    INFO Processing field field <class 'haystack.fields.CharField'>(short_description)
    WARNING Maybe te field has been already defined in the schema. Cause: Error from server: code=2200 [Invalid query] message="The search index schema is not valid because: Can't load schema schema.xml: [schema.xml] Duplicate field definition for 'short_description' [[[short_description{type=StrField,properties=indexed,omitNorms,omitTermFreqAndPositions}]]] and [[[short_description{type=TextField,properties=indexed,tokenized,stored}]]]"
    INFO Changing SEARCH INDEX field short_description to TextField
    INFO Processing field field <class 'haystack.fields.CharField'>(long_description)
    WARNING Maybe te field has been already defined in the schema. Cause: Error from server: code=2200 [Invalid query] message="The search index schema is not valid because: Can't load schema schema.xml: [schema.xml] Duplicate field definition for 'long_description' [[[long_description{type=StrField,properties=indexed,omitNorms,omitTermFreqAndPositions}]]] and [[[long_description{type=TextField,properties=indexed,tokenized,stored}]]]"
    ...
    ...

Generatic the static files
~~~~~~~~~~~~~~~~~~~~~~~~~~

We have some django extensions and the debug toolbar installed in DEBUG
mode. In order to them work we need to generate the static files.

::

    $ python manage.py collectstatic

The output should be something like:

::

    You have requested to collect static files at the destination
    location as specified in your settings:

        /...../myproject/static

    This will overwrite existing files!
    Are you sure you want to do this?

    Type 'yes' to continue, or 'no' to cancel: yes

    0 static files copied to '/..../myproject/static', 184 unmodified.

Setup the admin user
~~~~~~~~~~~~~~~~~~~~

Let's create the admin user with its own auth token

::

    $ python manage.py createsuperuser --username _myproject --email myproject@buildgroupai.com --noinput
    $ python manage.py changepassword _myproject
    Changing password for user '_myproject'
    Password:

A token will be created automatically for the user. We can get it back
using the following request:

::

    $ curl -H "Content-Type: application/json" -X POST \
        -d '{"username": "_myproject", "password": "MY_PASSWORD"}' \
        http://127.0.0.1:8001/api-token-auth/

    {"token":"b10061d0b62867d0d9e3eb4a8c8cb6a068b2f14a","user_id":1,"email":"myproject@buildgroupai.com"}

Deploy the crawling project into Google App Engine
--------------------------------------------------

The following section will explain what we need to do in order to deploy
our crawling project into GAE.

First, we need to be sure our production environment is up and running.
We will need a Google project with the following services ready:

-  A DSE cluster
-  A Redis server
-  A PostgreSQL server

Once these services are ready, we can start the deploy process.

1. We need to create a ``myproject`` user in PostgreSQL. We will need
   the password in the 3rd step.

2. Create a ``custom-flex-app.yaml`` based on the
   ``custom-flex-app.yaml.template``.

3. Edit the new ``custom-flex-app.yaml`` and set the correct values for
   all the environment variables. Ex:

   ::

       # [START runtime]
       runtime: custom
       env: flex
       entrypoint: ./docker-entrypoint.sh

       service: harvest

       runtime_config:
         python_version: 3

       automatic_scaling:
         min_num_instances: 1
         max_num_instances: 5
         cool_down_period_sec: 180
         cpu_utilization:
           target_utilization: 0.7

       resources:
         cpu: 1
         memory_gb: 1
         disk_size_gb: 10

       network:
         instance_tag: harvest-service

       beta_settings:
           cloud_sql_instances: dotted-ranger-212213:europe-west2:postgres-db

       env_variables:
         SECRET_KEY: $h5)b@2b4ts8lhzpl0ui@219jc5e%@ppewwd&i^wo1+1nregos

         STATIC_URL: https://storage.googleapis.com/static-harvest-${GAE_VERSION}/static/

         DEBUG: False

         THROTTLE_ENABLED: True

         SECURE_SSL_HOST:
         SECURE_SSL_REDIRECT: True

         # We are using the local pgbouncer connection pool
         DB_HOST: dotted-ranger-212213:europe-west2:postgres-db
         DB_PORT: 5432
         DB_USER: harvest
         DB_PASSWORD: sQQE87Nt

         HAYSTACK_URL: http://cassandra:sQQE87Nt@gasp-datastax-europe-west2-a-1-vm:8983/solr
         HAYSTACK_ADMIN_URL: http://cassandra:sQQE87Nt@gasp-datastax-europe-west2-a-1-vm:8983/solr/admin/cores

         CASSANDRA_DB_HOST: gasp-datastax-europe-west2-a-1-vm,gasp-datastax-europe-west2-a-2-vm,gasp-datastax-europe-west2-a-3-vm
         CASSANDRA_DB_NAME: harvest
         CASSANDRA_DB_USER: cassandra
         CASSANDRA_DB_PASSWORD: sQQE87Nt
         CASSANDRA_DB_STRATEGY: SimpleStrategy
         CASSANDRA_DB_REPLICATION: 3

         REDIS_HOST_PRIMARY: redis-vm
         REDIS_PORT_PRIMARY: 6379
         REDIS_PASS_PRIMARY: GeeCg1SqY7Lb

         EMAIL_HOST_USER: info@buildgroupai.com
         EMAIL_HOST_PASSWORD: 6ZREm4he

       # Google App Engine limits application deployments to 10,000 uploaded files per
       # version. The skip_files section allows us to skip virtual environment files
       # to meet this requirement. The first 5 are the default regular expressions to
       # skip, while the last one is for all env/ files.
       skip_files:
       - ^(.*/)?#.*#$
       - ^(.*/)?.*~$
       - ^(.*/)?.*\.py[co]$
       - ^(.*/)?.*/RCS/.*$
       - ^(.*/)?\..*$
       - ^env/.*$
       # [END runtime]

Run the crawler
---------------

Before start the crawler we need to have ready the responses for the
following questions:

-  The name of our crawler. Ex. ``my_crawler``

-  Where is located the binary of the Chromium library in our local
   system? Ex. ``/Applications/Chromium.app/Contents/MacOS/Chromium``

-  Where is the place in our local filesystem that is goin to be used as
   local - volatile - cache? Ex. ``fs:///data/harvest/local``

-  We are going to use Google Storage as permanent storage for our
   permanent cache? If yes, then we need to know the google project. Ex.
   ``centering-badge-212119``

-  The location we will use as permanent storage for our permanent
   cache. Ex. ``gs://my_crawler_cache``

-  How many workers we are going to start? Ex. ``10``

After responde these questions we are ready to run the crawler:

::

    python manage.py crawl myproject \
        --workers-num 10 \
        --chromium-bin-file '/Applications/Chromium.app/Contents/MacOS/Chromium' \
        --io-gs-project centering-badge-212119 \
        --cache-dir "gs://my_crawler_cache" \
        --local-dir "fs:///data/my_crawler/local"

Build the Docker image
----------------------

If we want to launch the crawler/s as docker containers we will need to
generate its docker image.

::

    $ docker build -t buildgroupai.com/davinci_crawler/myproject:0.1 .

Run the web application using Docker
------------------------------------

The project have been configured to run inside a docker container and
Google APP Engine.

The container is auto-sufficient, it starts the gunicorn workers, and
the pgbouncer proxy for PostgreSQL.

The unique required external services are:

-  Redis Server (we can start a server using docker:
   ``docker run -d --name myproject-redis -p 6379:6379 redis:3.0``)
-  PostgreSQL Server (using the ``CloudSQL Proxy``, a local PostgreSQL
   server with or without docker, or similar)
-  DataStax Enterprise or Cassandra Cluster (using production cluster, a
   local cluster (CCM), or similar)

To build the image we only need to execute the command:

::

    docker build -t gcr.io/centering-badge-212119/myproject:0.1 .

After the build, if you want to remove all the intermediate images that
docker generates, you can run the following command:

::

    $ docker rmi $(docker images -f "dangling=true" -q)

We can configure our container at start setting values for some
environment variables.

Some of these variables configure the access to the external services
commented before.

These are all the available environment variables we can use to
customize the server:

-  ``SECRET_KEY``: the secret key used to generate csrf tokens and
   secure your forms, for generate authentication tokens, and secured
   cookies.

-  ``DSE_SUPPORT``: are we working using a DataStax Enterprise Cluster?

-  ``DEBUG``: if we want to start the Django server in Debug mode

-  ``THROTTLE_ENABLED``: if we activate the api throttling mechanism

-  ``SECURE_SSL_REDIRECT``: are we executing the sever through SSL?
   (https)
-  ``SECURE_SSL_HOST``: the SSL host name

-  ``STATIC_URL``: the url to the static resources. By default we use
   the resources inside the image (nginx). In production, for instance,
   we will use th GS bucket.
   Ex.\ ``https://storage.googleapis.com/static-sky/static/``

-  ``REDIS_HOST_PRIMARY``: the host with a Redis server running on it
-  ``REDIS_PORT_PRIMARY``: the port at which the Redis server is
   listening for connections
-  ``REDIS_PASS_PRIMARY``: the password to use when connecting to the
   Redis server

-  ``DB_HOST``: the host with the PostgreSQL server running on it
-  ``DB_PORT``: the port at which the PostfreSQL server is listening for
   connections
-  ``DB_USER``: the user to use when connecting to the PostgreSQL server
-  ``DB_PASSWORD``: the password of the user we use to connect to the
   PostgreSL server

-  ``CASSANDRA_DB_HOST``: the host with the PostgreSQL server running on
   it
-  ``CASSANDRA_DB_NAME``: the port at which the PostfreSQL server is
   listening for connections
-  ``CASSANDRA_DB_USER``: the user to use when connecting to the
   PostgreSQL server
-  ``CASSANDRA_DB_PASSWORD``: the password of the user we use to connect
   to the PostgreSL server
-  ``CASSANDRA_DB_STRATEGY``: the password of the user we use to connect
   to the PostgreSL server
-  ``CASSANDRA_DB_REPLICATION``: the password of the user we use to
   connect to the PostgreSL server

-  ``HAYSTACK_URL``: the URL that give us access to the DSE/Solr service
   to execute queries directly into Solr.
-  ``HAYSTACK_ADMIN_URL``: the Admin URL to the DSE/Solr service

-  ``GOOGLE_ANALYTICS_ID``: our Google Analytics ID

-  ``ENV EMAIL_HOST_USER``: email user to use when sending emails
-  ``ENV EMAIL_HOST_PASSWORD``: the password of the user used to send
   emails

A ``environment.sh.template`` can be found at the root of the project.
You can rename the file to a normal shell file (.sh) and customize the
values of the variables based on your own environment.

Cassandra cluster (or DSE) is usually working as a cluster in your host
machine using maybe the CCM utility, not using docker. For that reason
we need to create aliases to the ``lo`` network IPs to IPs that Docker
can communicate with inside the containers.

The official docs of Docker, makes reference to an special IP This is
the IP that was referred to the official docs of docker.

This could be an example of how to start the server taking the following
assumptions into consideration:

-  We have the CloudSQL Proxy service started. It registers the server
   in the ip ``10.200.10.1``\ and port ``5433``.
-  A Redis 3.0 server running as a container in docker listening at the
   standard port ``6379``.
-  The BGDS API (Apian server) running in production and listening at
   ``https://bgds.io``.

To allow access from the sky container to the host PostgreSQL database
set by the CouldSQL Proxy we will need to do some things.

-  We need to create a new lo0 IP address 10.200.10.1 to the Mac. This
   is the IP that was referred to the official docs of docker.

::

    sudo ifconfig lo0 alias 10.200.10.1/24

-  We can check the new IP:

::

    $ ifconfig
    lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
        options=1203<RXCSUM,TXCSUM,TXSTATUS,SW_TIMESTAMP>
        inet 127.0.0.1 netmask 0xff000000
        inet6 ::1 prefixlen 128
        inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1
        inet 10.200.10.1 netmask 0xffffff00
        nd6 options=201<PERFORMNUD,DAD>

-  Once we have the IP ready we start the SQLCloud Proxy attached to
   this IP:

::

    $ cloud_sql_proxy -instances=centering-badge-212119:europe-west1:sky-pre-s=tcp:10.200.10.1:5433
    2018/08/29 19:34:02 Listening on 10.200.10.1:5433 for centering-badge-212119:europe-west1:sky-pre-s
    2018/08/29 19:34:02 Ready for new connections

Now we are ready to start the service:

::

    docker run -d --link=redis_bgds_db:redis \
        -p 8080:8080 \
        -e REDIS_HOST_PRIMARY='redis' \
        -e SKY_DB_HOST='10.200.10.1' \
        -e SKY_DB_PORT=5433 \
        -e DEBUG=False \
        -e COMPRESS_ENABLED=True \
        -e COMPRESS_OFFLINE=True \
        -e STATIC_URL="https://storage.googleapis.com/static-sky/static/" \
        --name sky \
        gcr.io/centering-badge-212119/sky:v2018-09

We can check the startup logs running the following command:

::

    docker logs -f sky

At this moment we should have ``gunicorn`` listening at the ``8000``
port, a ``daphne`` server at ``9000``, and the ``nginx`` at ``8080``.

We can open a browser and navigate to the following url:

::

    http://localhost:8080

**IMPORTANT**: We can use the environment variables to play with
different production environments. For instance, we can start the server
in mode ``Debug=True`` and without ``Compression=Fale`` to debug the
application simulating a production environment. We need to be careful
with variables like the ``Google Analytics ID``, if we use the
production ID for testing or developing purposes we will damage the real
statistics.

Deploy into production
----------------------

To do the deployment we use the ``bin/deploy.sh`` script. In this script
we will find all the logic behind a deployment. Basically, the steps are
done in the script are:

1. Prepare a ``gs bucket`` (Google Storage) to upload all the static
   files (``static-sky``).
2. Give public access to the ``gs bucket``.
3. Configure ``CORS`` to allow access to the static files from different
   origins
4. Prepare the production settings.py, setting the correct
   ``STATIC_URL`` for production (that uses
   ``https://storage.googleapis.com/static-sky/static/``), the ``DEBUG``
   to ``False``, the ``COMPRESS_ENABLED`` to ``True``, etc.
5. Compile the Django i18n message files
6. Collect the statics to put them into the ``/static`` folder
7. Compress the files
8. Copy (or rsync) the static file into the ``gs`` bucket.
9. Prepare the ``requirements.txt`` file using the
   ``requirements.txt.template`` file and making substitutions of the
   Github credentials (some dependencies are private).

The script also accepts some arguments:

-  ``-p, --project-name``: the id of the google project where we want to
   deploy the application.
-  ``-v, --version``: the version to use for the application we want to
   deploy. GAE allows us to manage multiple versions of our application.
-  ``-t, --type``: the GAE deployment environment to use. Today only
   ``flex`` deployments are allowed, we hope we can deploy the
   application in a standard environment soon
-  ``-d, --debug``: if we want to deploy the application with debug
   enabled.

