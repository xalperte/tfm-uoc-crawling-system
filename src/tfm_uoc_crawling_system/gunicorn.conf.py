# -*- coding: utf-8 -*
# Copyright (c) 2018-2019 BuildGroup Data Services Inc.
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.

##############################################################################
# gunicorn.conf
###############################################################################

import multiprocessing

# Server Socket
###############################################################################
# bind = '0.0.0.0:8000'
backlog = 2048

###############################################################################
# Worker Processes
###############################################################################
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000
max_requests = 0
timeout = 30
keepalive = 5

###############################################################################
# HTTPS and forwarding proxies
###############################################################################
forwarded_allow_ips = '*'
secure_scheme_headers = {'X-Forwarded-Proto': 'https'}

###############################################################################
# Debug
###############################################################################
debug = False
spew = False

###############################################################################
# Server Mechanics
###############################################################################
preload_app = False
daemon = False
pidfile = '/var/run/tfm_uoc_crawling_system.pid'
user = 'root'
group = 'root'
umask = 0
tmp_upload_dir = '/tmp'

###############################################################################
# Logging
###############################################################################
accesslog = '/var/log/tfm_uoc_crawling_system_access.log'
access_logformat = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" ' \
                   '"%(a)s"'
errorlog = '/var/log/tfm_uoc_crawling_system_s_error.log'
loglevel = 'info'
logger_class = 'simple'

###############################################################################
# Process Naming
###############################################################################
proc_name = 'tfm_uoc_crawling_system'
