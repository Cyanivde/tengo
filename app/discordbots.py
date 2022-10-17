import discord
import asyncio
from datetime import datetime
import os
from app.utils import _update_resource_num_comments_and_time, _update_resource_discord_link


class DiscordClientForMovingChannels(discord.Client):
    db = None

    def __init__(self, db):
        intents = discord.Intents.default()
        intents.guild_messages = True
        intents.guilds = True
        intents.message_content = True
        super().__init__(intents=intents)
        self.do = False
        self.db = db

    async def on_message(self, message):
        try:
            channel = message.channel
            if channel.position != 0:
                await channel.edit(position=0)

            resource_id = channel.topic.split('/')[-1][:-1]

            count = 0
            async for _ in channel.history(limit=None):
                count += 1

            _update_resource_num_comments_and_time(self.db, resource_id, count, datetime.now())
        except Exception as e:
            print(repr(e))

    async def on_guild_channel_create(self, channel):
        try:
            resource_id = channel.topic.split('/')[-1][:-1]
            _update_resource_discord_link(self.db, resource_id, channel.jump_url)
        except Exception as e:
            print(repr(e))


def create_discord_bot_for_moving_channels(db):
    client = DiscordClientForMovingChannels(db)
    asyncio.run(client.start(os.environ.get("DISCORD_TOKEN_2")))
