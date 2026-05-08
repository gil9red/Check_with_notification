#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "Стас Ай, Как Просто!".

"""


from pathlib import Path

from formats import FORMATS_VIDEO
from root_common import run_notification_job_rutube

run_notification_job_rutube(
    name="Стас Ай, Как Просто!",
    script_dir=Path(__file__).resolve().parent,
    url="https://rutube.ru/channel/21014334/videos/",
    formats=FORMATS_VIDEO.replace(
        prefix="🧐",
    ),
)
