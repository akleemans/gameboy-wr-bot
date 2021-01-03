#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from tools import game_platforms, download


def update_gb_games():
    """ Update list of gameboy platform games """
    print('[fetch.py::update_gb_games] Updating GB games list')
    gb_games = []
    for platform in game_platforms:
        content = download(
            f'https://www.speedrun.com/api/v1/games?platform={platform}&_bulk=yes&max=1000')
        gb_games.extend([entry['id'] for entry in content])
    gb_games = list(set(gb_games))
    print(f'[fetch.py::update_gb_games] Found {len(gb_games)} distinct games')

    with open('gb_games.json', 'w') as gb_games_file:
        gb_games_file.write(json.dumps(gb_games, indent=4))


if __name__ == "__main__":
    update_gb_games()
