#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from pathlib import Path


DIR: Path = Path(__file__).resolve().parent

SMS_TOKEN_FILE_NAME: Path = DIR / "SMS_TOKEN.txt"
SMS_TOKEN: str = (
    os.environ.get("SMS_TOKEN") or SMS_TOKEN_FILE_NAME.read_text("utf-8").strip()
)

# <API_ID>:<PHONE>
API_ID, TO = SMS_TOKEN.split(":")

FILE_NAME_SAVED: str = "saved.json"
FILE_NAME_SAVED_BACKUP: str = "saved_backup.json"
FILE_NAME_RUNS: str = "runs.json"

DEBUG_LOGGING_CURRENT_ITEMS: bool = False
DEBUG_LOGGING_GET_NEW_ITEMS: bool = False
