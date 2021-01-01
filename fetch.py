#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from typing import Dict, List

from tools import download, get_readable_time, gb_platforms

QUERY_GAME_AMOUNT = 100


def fetch_latest_wr_runs(fetch_all=False) -> List[Dict]:
    """ Fetch game leaderboards and check for new top runs """
    print('[fetch.py] Fetching runs, fetch_all=', fetch_all)
    try:
        with open('gb_games.json', 'r') as games_file:
            games = json.loads(games_file.read())
    except FileNotFoundError:
        games = []

    # Normal run: only check some chunk of games
    new_progress = 0
    if not fetch_all:
        progress = 0
        print('[fetch.py] Reading progress')
        try:
            with open('progress.json', 'r') as progress_file:
                progress = json.loads(progress_file.read())['progress']
            print(f'[fetch.py] Starting with progress={progress}')
        except FileNotFoundError:
            print(
                f'[fetch.py] Progress file not found, using progress={progress}')
        new_progress = (progress + QUERY_GAME_AMOUNT) % len(games)
        # If we passed the end, start from beginning
        if new_progress < progress:
            games = games[progress:] + games[:new_progress]
        else:
            games = games[progress:new_progress]

    print('[fetch.py] Reading leaderboards')
    try:
        with open('leaderboards.json', 'r') as leaderboards_file:
            leaderboards = json.loads(leaderboards_file.read())
    except FileNotFoundError:
        leaderboards = {}

    # Fetch current leaderboards for game
    wr_run_ids = []
    print(f'[fetch.py] Preparing to fetch {len(games)} games')
    for game_id in games:
        url = f'https://www.speedrun.com/api/v1/games/{game_id}/records?miscellaneous=no&scope=full-game&skip-empty=true&top=1'
        categories = download(url)

        current_game = {}
        for category in categories:
            category_id = category['category']
            top_run = category['runs'][0]['run']
            top_run_id = top_run['id']

            # If new game, new category or different run, it's a new WR
            if game_id not in leaderboards or category_id not in leaderboards[
                game_id] or leaderboards[game_id][category_id] != top_run_id:
                print(
                    f'Found new top run {top_run_id} for category {category_id} in game {game_id}')
                wr_run_ids.append(top_run_id)

            # Update current category with top run
            current_game[category_id] = top_run_id

        # Update current game entry
        leaderboards[game_id] = current_game

    # Fetch additional info for new WR runs
    wr_runs = []
    for run_id in wr_run_ids:
        print(f'[fetch.py] Found new WR: {run_id}, fetching info')
        url = f'https://www.speedrun.com/api/v1/runs/{run_id}?embed=game,players,category'
        wr_run = download(url)

        # Check if run itself was also on a platform we look for
        if wr_run['system']['platform'] not in gb_platforms:
            continue

        # Check if player is guest or not
        if wr_run['players']['data'][0]['rel'] == 'guest':
            player = wr_run['players']['data'][0]['name']
        else:
            player = wr_run['players']['data'][0]['names']['international']

        game_name = wr_run['game']['data']['names']['international']
        category = wr_run['category']['data']['name']
        image = wr_run['game']['data']['assets']['cover-small']['uri']
        primary_time = get_readable_time(wr_run['times']['primary'])
        wr_runs.append({'id': run_id, 'player': player, 'image': image,
                        'weblink': wr_run['weblink'],
                        'primary_time': primary_time,
                        'date-played': wr_run['date'], 'game': game_name,
                        'category': category})

    # Save progress
    with open('progress.json', 'w') as progress_file:
        progress_file.write(json.dumps({'progress': new_progress}, indent=4))

    # Save leaderboards
    with open('leaderboards.json', 'w') as leaderboards_file:
        leaderboards_file.write(json.dumps(leaderboards, indent=4))

    print('[fetch.py] Returning', len(wr_runs), 'WR runs.')
    return wr_runs


if __name__ == "__main__":
    fetch_latest_wr_runs()
