#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from pathlib import Path


DIR = Path(__file__).resolve().parent

SMS_TOKEN_FILE_NAME = DIR / "SMS_TOKEN.txt"
SMS_TOKEN = (
    os.environ.get("SMS_TOKEN") or SMS_TOKEN_FILE_NAME.read_text("utf-8").strip()
)

# <API_ID>:<PHONE>
API_ID, TO = SMS_TOKEN.split(":")

FILE_NAME_SAVED = "saved.json"
FILE_NAME_SAVED_BACKUP = "saved_backup.json"

DEBUG_LOGGING_CURRENT_ITEMS = False
DEBUG_LOGGING_GET_NEW_ITEMS = False
