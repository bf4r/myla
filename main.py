import discord
import os

bot_token = os.environ["MYLA_BOT_TOKEN"]

PREFIX = "."

def iscmd(message, cmdstr):
    return message.content.startswith(PREFIX + cmdstr);

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, msg):
        print(f"{msg.author}: {msg.content}")
        if iscmd(msg, "hey"):
            await msg.reply("hello")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(bot_token)
