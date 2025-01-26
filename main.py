import discord
import os

bot_token = os.environ["MYLA_BOT_TOKEN"]

PREFIX = "."

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
        if message.content.startswith(PREFIX + "hey"):
            await message.channel.send("hello")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(bot_token)
