import discord
from discord.ext import commands
from ai import ask_ai, switch_ai_chat, get_ai_chats
import os
from config import *

bot_token = os.environ.get("MYLA_BOT_TOKEN")

if not bot_token:
    print("Please set the MYLA_BOT_TOKEN environment variable with your Discord bot token from the Discord developer portal.\nWindows:\nset MYLA_BOT_TOKEN=...\nLinux:\nexport MYLA_BOT_TOKEN=...")
    exit(1)

# discord setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# helper that splits message every 2000 characters to get around the discord message character limit
async def reply(msg, text):
    max_msg_length = 2000
    parts = [text[i: i + max_msg_length] for i in range(0, len(text), max_msg_length)]
    for part in parts:
        await msg.reply(part)

@bot.command()
async def hey(ctx):
    await reply(ctx.message, "hello")

@bot.command()
async def ping(ctx):
    await reply(ctx.message, "pong!")

@bot.command()
async def aichats(ctx):
    chats = get_ai_chats(ctx.message)
    sb = ""
    for chat_name, chat in chats.items():
        sb += chat_name + f"\n  {len(chat['messages'])} messages\n"
    await reply(ctx.message, sb)

@bot.command()
async def aichat(ctx):
    switch_ai_chat(ctx.message)
    await reply(ctx.message, "switched chats")

@bot.command()
async def ai(ctx):
    response_text = await ask_ai(ctx.message)
    await reply(ctx.message, response_text)

def run():
    bot.run(bot_token)
