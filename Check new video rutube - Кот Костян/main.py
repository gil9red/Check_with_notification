#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "Кот Костян".

"""


from pathlib import Path

from formats import FORMATS_VIDEO
from root_common import run_notification_job_rutube

run_notification_job_rutube(
    name="Кот Костян",
    script_dir=Path(__file__).resolve().parent,
    url="https://rutube.ru/channel/5223991/videos/",
    formats=FORMATS_VIDEO.replace(
        prefix="😼",
    ),
)
