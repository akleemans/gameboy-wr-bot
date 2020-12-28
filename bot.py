import os
from datetime import datetime
from typing import Dict

import discord
from dotenv import load_dotenv

from fetch import fetch_latest_wr_runs

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()


def create_message(run: Dict) -> discord.Embed:
    """ Create embedded message from run info """
    title = f'{run["game"]} - {run["category"]}'
    description = f'{run["primary_time"]} by {run["player"]}'
    embedded_message = discord.Embed(title=description, color=0x00ff00,
                                     url=run['weblink'])
    embedded_message.set_thumbnail(url=run['image'])
    embedded_message.set_author(name=title)
    embedded_message.add_field(name='Date played', value=run['date-played'])
    today = datetime.now().strftime('%Y-%m-%d')
    embedded_message.set_footer(text=today)
    return embedded_message


@client.event
async def on_ready():
    print('[bot.py] Fetching new WR runs...')
    wr_runs = fetch_latest_wr_runs()

    print('[bot.py] Updating servers...')
    for server in client.guilds:
        print('[bot.py] Sending updates to server: ', server.name, '/',
              server.id)

        for channel in server.channels:
            if str(channel.type) == 'text' and 'gb-wr-bot' in str(channel):
                print('[bot.py] sending to channel:', channel)
                for run in wr_runs:
                    await channel.send(embed=create_message(run))

    print('[bot.py] All done, going back to sleep.')
    await client.logout()


client.run(TOKEN)
