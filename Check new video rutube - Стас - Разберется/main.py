#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "Стас разберется".

"""


from pathlib import Path

from formats import FORMATS_VIDEO
from root_common import run_notification_job_rutube

run_notification_job_rutube(
    name="Стас разберется",
    script_dir=Path(__file__).resolve().parent,
    url="https://rutube.ru/plst/526955/",
    formats=FORMATS_VIDEO.replace(
        prefix="🧐",
    ),
)
