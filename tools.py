#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import math
import time
from typing import Dict, List, Union

import isodate
import requests

# All GB platforms we want to check
gb_platforms = [
    'n5683oev',  # Game Boy
    'vm9v3ne3',  # Game Boy Interface
    '7m6yvw6p',  # Game Boy Player
    '3167jd6q',  # Super Game Boy
    'n5e147e2',  # Super Game Boy 2
]


def download(url: str) -> Union[List, Dict]:
    """ Download data from SRC API, with throttling """
    print('[tools.py::download] Fetching', url)
    time.sleep(0.8)
    headers = {'user-agent': 'akleemans-gameboy-wr-bot/2.0'}
    content = ''
    try:
        content = json.loads(requests.get(url, headers=headers).text)
        data = content['data']
    except KeyError as e:
        print('[tools.py::download] ERROR: no data attribute in', content)
        return []
    except:
        print('[tools.py::download] ERROR: other error occurred')
        return []
    else:
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
