import os
import discord
from datetime import datetime

from pytz import utc
from dubai_iacad_scraper import DubaiIacadPrayerTimes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
scraper = DubaiIacadPrayerTimes()
client = discord.Client()


def get_general_channels(guild):
    return [channel for channel in guild.text_channels if channel.name == 'general']


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print([f'{guild.name}' for guild in client.guilds])

    for channel in get_general_channels(client.guilds[0]):
        await channel.send(f"nearest prayer in Dubai is {scraper.prayer_tuple_to_str(scraper.get_nearest_prayer())} \
            which is in {((scraper.get_nearest_prayer()[1] - datetime.now(utc)).seconds/60):d} minutes")

if __name__ == "__main__":
    client.run(TOKEN)
