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
    # 'gde3g9k1',  # Game Boy Color
    # '3167d6q2',  # Game Boy Advance
    'vm9v3ne3',  # Game Boy Interface
    '7m6yvw6p',  # Game Boy Player
    '3167jd6q',  # Super Game Boy
    'n5e147e2',  # Super Game Boy 2
]


def download(url: str) -> Union[List, Dict]:
    print('[fetch.py::download] Fetching', url)
    content = ''
    try:
        content = json.loads(requests.get(url).text)
        data = content['data']
    except KeyError as e:
        print('[fetch.py::download] ERROR: no data attribute in', content)
        return []
    except:
        print('[fetch.py::download] ERROR: other error occurred')
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


def fetch_latest_wr_runs() -> List[Dict]:
    """ Fetch recently verified runs """
    print('[fetch.py] Fetching latest runs')
    latest_runs = []
    start_time = time.time()
    for platform in gb_platforms:
        url = f'https://www.speedrun.com/api/v1/runs?status=verified&platform={platform}&orderby=verify-date&direction=desc'
        platform_runs = download(url)
        latest_runs.extend(platform_runs)
    print('[fetch.py] Fetched all platforms in',
          round(time.time() - start_time, 2), 's')

    print('[fetch.py] Reading known runs')
    try:
        with open('known_runs.json', 'r') as known_runs_file:
            known_runs = json.loads(known_runs_file.read())
        known_ids = [run['id'] for run in known_runs]
    except FileNotFoundError:
        known_ids = []

    # Check for WR runs
    wr_runs = []
    for run in latest_runs:
        # Skip known runs
        if run['id'] in known_ids:
            continue
        # Don't check single level runs
        if run['level'] != None:
            continue

        print('[fetch.py] Checking run', run['weblink'])
        url = 'https://www.speedrun.com/api/v1/leaderboards/' + \
              run['game'] + '/category/' + run['category'] + '?top=1'
        category_runs = download(url)
        first_place = category_runs['runs'][0]['run']
        if run['id'] == first_place['id']:
            print('[fetch.py] Found new WR:', run['weblink'], 'fetching info')
            url = f'https://www.speedrun.com/api/v1/runs/{run["id"]}?embed=game,players,category'
            wr_run = download(url)
            game_name = wr_run['game']['data']['names']['international']
            player = wr_run['players']['data'][0]['names']['international']
            category = wr_run['category']['data']['name']
            image = wr_run['game']['data']['assets']['cover-small']['uri']
            primary_time = get_readable_time(wr_run['times']['primary'])
            wr_runs.append({'id': run['id'], 'player': player, 'image': image,
                            'weblink': wr_run['weblink'],
                            'primary_time': primary_time,
                            'date-played': wr_run['date'], 'game': game_name,
                            'category': category})

    # Save new runs as known runs for future reference
    with open('known_runs.json', 'w') as known_runs_file:
        known_runs_file.write(json.dumps(latest_runs, indent=4))
    print('[fetch.py] Returning', len(wr_runs), 'WR runs.')
    return wr_runs


if __name__ == "__main__":
    fetch_latest_wr_runs()
