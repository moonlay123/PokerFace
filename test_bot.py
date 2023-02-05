import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        content = message.content
        if content != '':
            print(content)
            await MyClient.print_chat(self, content)
            await MyClient.print_pm(self, content, message.author)

    async def print_chat(self, content):
        channel = self.get_channel(1054425075731939378)
        await channel.send(content)

    async def print_pm(self, content, user):
        await user.send(content)





activity = discord.Game(name="Texas hold'em")
client = MyClient(intents=discord.Intents.default(), activity=activity)
token = open('token.txt', 'r').readline()
client.run(token)

