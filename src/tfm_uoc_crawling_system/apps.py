# -*- coding: utf-8 -*
# Copyright (c) 2018-2019 BuildGroup Data Services Inc.
# All rights reserved.

from django.apps import AppConfig


class DaVinciCrawlerConfig(AppConfig):
    name = 'tfm_uoc_crawling_system'
    verbose_name = "Django DaVinci Crawler tfm_uoc_crawling_system"

    def ready(self):
        pass
        # Add System checks
        # from .checks import pagination_system_check  # NOQA
