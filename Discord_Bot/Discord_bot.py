import discord
from discord import utils

import config

class MyClient(discord.Client):
    async def on_ready(self):
        print('Loffed on as  {0}!'.format(self.user))

    async def on_raw_reactions_add(self, payload):
        channel = self.get_channel(payload.channel_id)
        pass

    async def on_raw_reactions_remove(self, payload):
        pass


client = MyClient()
client.run(#Token)

client.run(comfig.TOKEN)
