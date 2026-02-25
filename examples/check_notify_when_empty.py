#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для проверки notify_when_empty.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import NotificationJob, run_notification_job


# Process error
run_notification_job(
    "Тест",
    DIR,
    lambda _: [],
    is_single=True,
    timeout_for_when_empty_seconds=1,
    max_attempts_for_when_empty=3,
    need_notification=False,
)

print("\n" + "-" * 100 + "\n")

# Process OK
run_notification_job(
    "Тест",
    DIR,
    lambda _: ["123"],
    is_single=True,
    timeout_for_when_empty_seconds=1,
    max_attempts_for_when_empty=3,
    need_notification=False,
)

print("\n" + "-" * 100 + "\n")


# Process OK on second attempt
def on_start(job: NotificationJob) -> None:
    job.attempts = 0


def on_start_check(job: NotificationJob) -> None:
    job.attempts += 1


def get_new_items(job: NotificationJob):
    return ["123"] if job.attempts == 2 else []


run_notification_job(
    "Тест",
    DIR,
    get_new_items,
    is_single=True,
    timeout_for_when_empty_seconds=1,
    max_attempts_for_when_empty=3,
    need_notification=False,
    callbacks=NotificationJob.Callbacks(
        on_start=on_start,
        on_start_check=on_start_check,
    ),
)
