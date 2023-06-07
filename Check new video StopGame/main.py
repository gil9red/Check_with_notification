#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео из конкретных плейлистов канала StopGame.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    run_notification_job,
    SavedModeEnum,
    get_video_list_from_playlists,
)


PLAYLISTS = [
    (f"История серии Diablo", "PLZfhqd1-Hl3DtfKRjleAWB-zYJ-pj7apK"),
    (f"История серии Final Fantasy", "PLZfhqd1-Hl3DnNDG-x6SgDqlBJee-50E1"),
    (f"История серии Metroid", "PLZfhqd1-Hl3Di2yxyrrvH53vdREDrHU3c"),
    (f"История серии The Elder Scrolls", "PLZfhqd1-Hl3C0B3dmwhuKKzUJ-H30gGVj"),
    (f"За кадром", "PLZfhqd1-Hl3BEdYEAhuq62G5fRLtSXbJ9"),
    (f"Разбор полётов", "PLZfhqd1-Hl3BKhWwCgmqtENSlearqLlAV"),
    (f"Спидран в деталях", "PLZfhqd1-Hl3D5Y_DW3fD9lyaclvt89XsI"),
    (f"Страшно, вырубай!", "PLZfhqd1-Hl3CdAaP_DVgU2tpBSVLBNICD"),
    (f"Уэс и Флинн", "PLZfhqd1-Hl3C5AQ6LPcMsVBIpduqckjPB"),
    (f"Хардмод", "PLZfhqd1-Hl3BCuapQSaNrNyDAy3wLiOLL"),
]


run_notification_job(
    "StopGame",
    DIR,
    lambda job: get_video_list_from_playlists(job, PLAYLISTS),
    save_mode=SavedModeEnum.DATA_ITEM,
    # Чтобы не было "каши", т.к. видео собирается из нескольких плейлистов
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
