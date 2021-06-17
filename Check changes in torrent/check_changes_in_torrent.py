#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Script for download serial torrent by qbittorrent.
When serial torrent modify (example: append new series), script download new files.

"""


import re
import time
import traceback
import sys

from collections import defaultdict
from datetime import datetime
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

import effbot_bencode
import requests

from bs4 import BeautifulSoup
from qbittorrent import Client

from root_common import wait, simple_send_sms


def get_rutor_torrent_download_info(torrent_url):
    """
    Parse torrent url and return tuple: (torrent_file_url, magnet_url, info_hash)

    """

    rs = requests.get(torrent_url)
    root = BeautifulSoup(rs.content, 'lxml')

    magnet_url = root.select_one('#download > a[href^="magnet"]')['href']

    # For get info hash from magnet url
    match = re.compile(r'btih:([abcdef\d]+?)&', flags=re.IGNORECASE).search(magnet_url)
    if match:
        raise Exception('Not found "info hash" from magnet url!')

    info_hash = match.group(1)

    return torrent_url.replace('/torrent/', '/download/'), magnet_url, info_hash


def remove_previous_torrent_from_qbittorrent(qb, new_info_hash):
    info_hash_by_name_dict = {torrent['hash']: torrent['name'] for torrent in qb.torrents()}

    name_by_info_hash_list_dict = defaultdict(list)

    for info_hash, name in info_hash_by_name_dict.items():
        name_by_info_hash_list_dict[name].append(info_hash)

    # If info_hash already in torrent list
    if new_info_hash in info_hash_by_name_dict:
        # Get torrent name
        name = info_hash_by_name_dict[new_info_hash]

        # Get torrents info hash with <name>
        info_hash_list = name_by_info_hash_list_dict[name]

        # Remove new (current) info hash
        info_hash_list.remove(new_info_hash)

        # Remove previous torrents
        if info_hash_list:
            print('Удаление предыдущих раздач этого торрента: {}'.format(info_hash_list))
            qb.delete(info_hash_list)

    else:
        print("Предыдущие закачки не найдены")


if __name__ == '__main__':
    IP_HOST = 'http://127.0.0.1:8080/'
    USER = 'admin'
    PASSWORD = '<PASSWORD>'

    qb = Client(IP_HOST)
    qb.login(USER, PASSWORD)

    torrent_url = 'http://anti-tor.org/torrent/544942'

    last_info_hash = None
    last_torrent_files = []

    while True:
        try:
            today = datetime.today()

            torrent_file_url, _, info_hash = get_rutor_torrent_download_info(torrent_url)
            print(f'{today}: Проверка {torrent_url}: {torrent_file_url} / {info_hash}')

            if qb.get_torrent(info_hash):
                print(f'Торрент {info_hash} уже есть в списке раздачи')

            else:
                if info_hash != last_info_hash:
                    data = requests.get(torrent_file_url).content.decode('latin1')

                    torrent = effbot_bencode.decode(data)
                    files = ["/".join(file["path"]) for file in torrent["info"]["files"]]

                    # Использование множеств, чтобы узнать разницу списков, т.е. какие файлы были добавлены
                    # А чтобы узнать какие были удалены: list(set(last_torrent_files) - set(files))
                    new_files = list(set(files) - set(last_torrent_files))

                    if last_info_hash is None:
                        print(f"Добавление торрента с {len(new_files)} файлами: {new_files}")
                    else:
                        print('Торрент изменился, пора его перекачивать')
                        print(f"Добавлено {len(new_files)} файлов: {new_files}")

                    last_info_hash = info_hash
                    last_torrent_files = files

                    # Say qbittorrent client download torrent file
                    # OR: qb.download_from_file
                    qb.download_from_link(torrent_file_url)

                    # Отправляю смс на номер
                    text = f"Вышла новая серия '{torrent['info']['name']}'"
                    simple_send_sms(text)

                    # Даем 5 секунд на добавление торрента в клиент
                    time.sleep(5)

                    remove_previous_torrent_from_qbittorrent(qb, info_hash)

                else:
                    print('Изменений нет')

            print()

            # Every 3 hours
            wait(hours=3)

        except Exception:
            print('Ошибка:')
            print(traceback.format_exc())

            print('Через 5 минут попробую снова...')

            # Wait 1 minute before next attempt
            time.sleep(60)
