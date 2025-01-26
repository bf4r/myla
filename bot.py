import discord
from ai import ask_ai, switch_ai_chat
import os
from config import *

bot_token = os.environ.get("MYLA_BOT_TOKEN")

if not bot_token:
    print("Please set the MYLA_BOT_TOKEN environment variable with your Discord bot token from the Discord developer portal.\nWindows:\nset MYLA_BOT_TOKEN=...\nLinux:\nexport MYLA_BOT_TOKEN=...")
    exit(1)

def iscmd(msg, cmdstr):
    return msg.content.startswith(COMMAND_PREFIX + cmdstr);

class BotClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, msg):
        print(f"{msg.author}: {msg.content}")
        if iscmd(msg, "hey"):
            await msg.reply("hello")
        elif iscmd(msg, "ping"):
            await msg.reply("pong!")
        elif iscmd(msg, "aichat"):
            switch_ai_chat(msg)
            await msg.reply("switched chats")
        elif iscmd(msg, "ai"):
            response_text = await ask_ai(msg)
            max_msg_length = 2000
            parts = [response_text[i: i + max_msg_length] for i in range(0, len(response_text), max_msg_length)]
            for part in parts:
                await msg.reply(part)

def run():
    # discord setup
    intents = discord.Intents.default()
    intents.message_content = True

    # run the bot
    bot_client = BotClient(intents=intents)
    bot_client.run(bot_token)
