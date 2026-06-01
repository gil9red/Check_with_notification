#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "МАКСИМОВИЧ".

"""


from pathlib import Path
from root_common import run_notification_job_rutube

run_notification_job_rutube(
    name="МАКСИМОВИЧ",
    script_dir=Path(__file__).resolve().parent,
    url="https://rutube.ru/channel/26578985/videos/",
)
