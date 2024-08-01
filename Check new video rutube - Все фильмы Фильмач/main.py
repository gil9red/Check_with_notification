#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео из плейлиста "Все фильмы" из Фильмач в Rutube.

"""


from pathlib import Path
from root_common import run_notification_job_rutube_many


run_notification_job_rutube_many(
    name="Все фильмы Фильмач [Rutube]",
    script_dir=Path(__file__).resolve().parent,
    url="https://rutube.ru/plst/328068/",
)
