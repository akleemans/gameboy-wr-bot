#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import math
import time
from datetime import datetime
from typing import Dict, List, Union

import isodate
import requests

DATE_FORMAT_SRC = '%Y-%m-%dT%H:%M:%SZ'

# Game must have one of these platforms to be tracked
game_platforms = [
    'n5683oev',  # Game Boy
    '3167jd6q',  # Super Game Boy
    'n5e147e2',  # Super Game Boy 2
]

# Run itself must have one of these platforms to qualify
run_platforms = [
    'n5683oev',  # Game Boy
    'vm9v3ne3',  # Game Boy Interface
    '7m6yvw6p',  # Game Boy Player
    '3167jd6q',  # Super Game Boy
    'n5e147e2',  # Super Game Boy 2
    '8gejn93d',  # Wii U
    'v06dk3e4',  # Wii
    'nzelreqp',  # Wii Virtual Console
    '7g6mx89r',  # 3DS Virtual Console
]


def download(url: str) -> Union[List, Dict]:
    """ Download data from SRC API, with throttling """
    print('[tools.py::download] Fetching', url)
    time.sleep(1)
    headers = {'user-agent': 'akleemans-gameboy-wr-bot/2.0'}
    content = json.loads(requests.get(url, headers=headers).text)
    data = content['data']
    return data


def get_readable_time(duration: str) -> str:
    """ Converts ISO duration strings like 'PT52.250S' into a readable time """
    seconds = isodate.parse_duration(duration).total_seconds()
    ms = round(seconds % 1 * 1000)
    ss = math.floor(seconds % 60)
    mm = math.floor(seconds // 60 % 60)
    hh = math.floor(seconds // 3600)
    s = ''

    if hh > 0:
        s = f'{hh}h '
    if mm > 0:
        s += f'{mm}m '

    s += f'{ss}s'

    if ms > 0:
        s += f' {ms}ms'
    return s


def get_age(date1: str, date2: str) -> int:
    """ Calculate date difference in hours """
    d1 = datetime.strptime(date1, DATE_FORMAT_SRC)
    d2 = datetime.strptime(date2, DATE_FORMAT_SRC)
    if d1 > d2:
        diff = d1 - d2
    else:
        diff = d2 - d1
    return round(diff.seconds / 3600 + diff.days * 24)


def get_age_from_now(date: str) -> int:
    """ Calculate age (from today) in hours """
    now = datetime.now().strftime(DATE_FORMAT_SRC)
    return get_age(now, date)
