#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Почему нельзя победить [Звездный Капитан].

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    SavedModeEnum,
    get_vkvideo_video_list,
    run_notification_job,
)

run_notification_job(
    "Почему нельзя победить [Звездный Капитан] [vkvideo]",
    DIR,
    lambda _: get_vkvideo_video_list("https://vkvideo.ru/playlist/-119338402_3"),
    save_mode=SavedModeEnum.DATA_ITEM,
    formats=FORMATS_VIDEO.replace(
        prefix="💀",
    ),
)
