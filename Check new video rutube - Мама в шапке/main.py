#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "Мама в шапке".

"""


from pathlib import Path
from root_common import run_notification_job_rutube
from formats import FORMATS_VIDEO

run_notification_job_rutube(
    name="Мама в шапке",
    script_dir=Path(__file__).resolve().parent,
    url="https://rutube.ru/u/mamavshapke/videos/",
    formats=FORMATS_VIDEO.replace(
        prefix="👒",
    ),
)
