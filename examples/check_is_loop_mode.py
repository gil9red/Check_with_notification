#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для примера режима is_single.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

# Use argument
sys.argv.append("--loop")

from root_common import TimeoutWait, NotificationJob, run_notification_job


class StopException(Exception):
    pass


def on_start(job: NotificationJob) -> None:
    job.attempts = 0


def on_start_check(job: NotificationJob) -> None:
    job.attempts += 1


def get_new_items(job: NotificationJob):
    if job.attempts <= 2:
        return list(map(str, range(job.attempts)))

    job.is_single = True
    job.max_attempts_for_is_single = 0
    raise StopException("Stop!")


try:
    run_notification_job(
        "Тест",
        DIR,
        get_new_items,
        timeout=TimeoutWait(seconds=1),
        need_notification=False,
        callbacks=NotificationJob.Callbacks(
            on_start=on_start,
            on_start_check=on_start_check,
        ),
    )
except StopException as e:
    print(e)

print("\n" + "-" * 50 + "\n")

sys.argv.remove("--loop")
try:
    run_notification_job(
        "Тест",
        DIR,
        get_new_items,
        is_single=False,
        timeout=TimeoutWait(seconds=1),
        need_notification=False,
        callbacks=NotificationJob.Callbacks(
            on_start=on_start,
            on_start_check=on_start_check,
        ),
    )
except StopException as e:
    print(e)

print("\n" + "-" * 50 + "\n")

# Process error
def get_new_items_with_exc(job: NotificationJob):
    if job.attempts <= 2:
        return [str(1 / 0)]

    job.is_single = True
    job.max_attempts_for_is_single = 0
    raise StopException("Stop!")

run_notification_job(
    "Тест",
    DIR,
    get_new_items_with_exc,
    is_single=False,
    timeout=TimeoutWait(seconds=1),
    timeout_exception_seconds=1,
    need_notification=False,
    callbacks=NotificationJob.Callbacks(
        on_start=on_start,
        on_start_check=on_start_check,
    ),
)
