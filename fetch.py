import json
import math
import time
from datetime import datetime
from typing import Dict, List

import isodate
import requests

# All GB platforms we want to check
gb_platforms = [
    'n5683oev',  # Game Boy
    'gde3g9k1',  # Game Boy Color
    '3167d6q2',  # Game Boy Advance
    'vm9v3ne3',  # Game Boy Interface
    '7m6yvw6p',  # Game Boy Player
    '3167jd6q',  # Super Game Boy
    'n5e147e2',  # Super Game Boy 2
]


def convert_runs(runs: List[Dict]) -> List[Dict]:
    """ Convert runs for saving them """
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    return [{'id': run['id'], 'verify-date': run['status']['verify-date'],
             'save-date': now} for run in runs]


def get_readable_time(duration: str) -> str:
    """ Converts ISO duration strings like 'PT52.250S' into a readable time """
    seconds = isodate.parse_duration(duration).total_seconds()
    minutes = seconds // 60
    hours = seconds // 3600
    s = ''
    if hours > 0:
        s = f'{hours}h '
    if minutes > 0:
        s += f'{math.floor(minutes % 60)}m '

    if seconds % 1 == 0:
        seconds = math.floor(seconds % 60)
    else:
        seconds = round(seconds % 60 * 100) / 100

    s += f'{seconds}s'
    return s


def fetch_latest_wr_runs() -> List[Dict]:
    """ Fetch recently verified runs """
    print('[fetch.py] Fetching latest runs')
    latest_runs = []
    start_time = time.time()
    for platform in gb_platforms:
        url = f'https://www.speedrun.com/api/v1/runs?status=verified&platform={platform}&orderby=verify-date&direction=desc'
        platform_runs = json.loads(requests.get(url).text)['data']
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
        category_runs = json.loads(requests.get(url).text)['data']
        first_place = category_runs['runs'][0]['run']
        if run['id'] == first_place['id']:
            print('[fetch.py] Found new WR:', run['weblink'], 'fetching info')
            url = f'https://www.speedrun.com/api/v1/runs/{run["id"]}?embed=game,players,category'
            wr_run = json.loads(requests.get(url).text)['data']
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
    known_runs = convert_runs(latest_runs)
    with open('known_runs.json', 'w') as known_runs_file:
        known_runs_file.write(json.dumps(known_runs, indent=4))
    print('[fetch.py] Returning', len(wr_runs), 'WR runs.')
    return wr_runs


if __name__ == "__main__":
    fetch_latest_wr_runs()
