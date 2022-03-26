import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Loffed on as  {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0, content}'. format(message))

client = MyClient()
client.run('OTU3MzUzMTY2MDg3NzkwNjEz.Yj9inQ.TSynjsU2CNxCoogd7qz1Hv24mWw')
