#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео сериала One Piece.

"""


from pathlib import Path
from root_common import run_notification_job_rutube


run_notification_job_rutube(
    name="Сериал One Piece",
    script_dir=Path(__file__).resolve().parent,
    url="https://rutube.ru/plst/320765/",
)
