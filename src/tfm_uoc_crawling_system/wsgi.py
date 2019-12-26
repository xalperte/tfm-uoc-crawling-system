# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 BuildGroup Data Services Inc.


"""
WSGI config for DaVinci project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from configurations.wsgi import get_wsgi_application

configuration = os.getenv('ENVIRONMENT', 'development').title()
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "tfm_uoc_crawling_system.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', configuration)

application = get_wsgi_application()
