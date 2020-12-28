# gameboy-wr-bot

Discord bot for tracking Game Boy related speedrun world records.

## How to use

1. Invite the bot via
   this [Bot invite link](https://discord.com/api/oauth2/authorize?client_id=792776699984216114&permissions=2048&scope=bot).
   It will need the "Send message" permission, obviously.
2. Have a channel with 'gb-wr-bot' in its name on your server. The bot will automatically post new
   WRs there!

Currently, the following speedrun.com platforms are tracked: GB, GBC, GBA, SGB, SGB2, GBP, and GBi.

## How it works

Periodically (all 5 mins), all new runs for the GB platforms (see above) are fetched and checked if
they are first place on their respective leaderboards. The run-ids are then cached so upon newer
fetching, it's clear whether the run is already known or a new one.

The bot is hosted by me, see below if you want to set up your own instance.

## Development

The Bot runs on (and was tested with) Python 3.8.

First, install the necessary Python libs:

    pip3 install -U requests discord.py python-dotenv isodate

Then apply your changes in the following files:

* `bot.py`: The "Bot"-part which connects to Discord.
* `fetch.py`: Accesses the [speedrun.com-API](https://github.com/speedruncomorg/api) and fetches the
  latest runs.
* `known_runs.json`: Save run IDs to check if a run was already processed (and notified).
This file will be created on the first run of the bot.

## Deployment

If you want to host a version of this Bot yourself, be sure to follow the following steps:

* Create an application and a bot on the [Discord Developer Portal](https://discord.com/developers/).
  There are good tutorials like for example on [realpython.com](https://realpython.com/how-to-make-a-discord-bot-python/).
* Create a `.env` file based on `.env-template` and enter the Bot token you got out of the Discord dev portal.
* Periodically trigger a run of `python3 bot.py`, for example with CRON. This will trigger fetching new
runs, connect to Discord and send out messages if there were new WRs. After that, it will automatically go back to sleep.
