#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Гоблина из плейлиста "Хазин и Пучков".

"""


from pathlib import Path
from root_common import run_notification_job_rutube

run_notification_job_rutube(
    name="Хазин и Пучков",
    script_dir=Path(__file__).resolve().parent,
    url="https://rutube.ru/plst/1444528/",
)
