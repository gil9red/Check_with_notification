#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path


DIR = Path(__file__).resolve().parent
LOCK_FILE = DIR / 'lock'


def set_lock(lock: bool):
    if lock:
        LOCK_FILE.touch(exist_ok=True)
    else:
        if has_lock():
            LOCK_FILE.unlink()


def has_lock() -> bool:
    return LOCK_FILE.exists()


if __name__ == '__main__':
    set_lock(True)
    assert has_lock()

    set_lock(False)
    assert not has_lock()
