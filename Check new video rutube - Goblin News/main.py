#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Гоблина из плейлиста "Goblin News".

"""


from pathlib import Path
from root_common import run_notification_job_rutube


run_notification_job_rutube(
    name="Goblin News",
    script_dir=Path(__file__).resolve().parent,
    url="https://rutube.ru/plst/199475/",
)
