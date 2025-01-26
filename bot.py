import discord
from ai import ask_ai, switch_ai_chat, get_ai_chats
import os
from config import *

bot_token = os.environ.get("MYLA_BOT_TOKEN")

if not bot_token:
    print("Please set the MYLA_BOT_TOKEN environment variable with your Discord bot token from the Discord developer portal.\nWindows:\nset MYLA_BOT_TOKEN=...\nLinux:\nexport MYLA_BOT_TOKEN=...")
    exit(1)

# starts with this
def iscmd(msg, cmdstr):
    return msg.content.startswith(COMMAND_PREFIX + cmdstr)

# exact match
def iscmde(msg, cmdstr):
    return msg.content == (COMMAND_PREFIX + cmdstr)

async def reply(msg, text):
    max_msg_length = 2000
    parts = [text[i: i + max_msg_length] for i in range(0, len(text), max_msg_length)]
    for part in parts:
        await msg.reply(part)

class BotClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, msg):
        print(f"{msg.author}: {msg.content}")
        if iscmde(msg, "hey"):
            await reply(msg, "hello")
        elif iscmde(msg, "ping"):
            await reply(msg, "pong!")
        elif iscmde(msg, "aichats"):
            chats = get_ai_chats(msg)
            sb = ""
            for chat_name, chat in chats.items():
                sb += chat_name + f"\n  {len(chat["messages"])} messages\n"
            await reply(msg, sb)
        elif iscmd(msg, "aichat"):
            switch_ai_chat(msg)
            await reply(msg, "switched chats")
        elif iscmd(msg, "ai"):
            response_text = await ask_ai(msg)
            await reply(msg, response_text)

def run():
    # discord setup
    intents = discord.Intents.default()
    intents.message_content = True

    # run the bot
    bot_client = BotClient(intents=intents)
    bot_client.run(bot_token)
