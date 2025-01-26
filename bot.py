import discord
from discord.ext import commands
from ai import *
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

@bot.command(help="Says hello")
async def hey(ctx):
    await reply(ctx.message, "hello")

@bot.command(help="Says pong!")
async def ping(ctx):
    await reply(ctx.message, "pong!")

@bot.command(help="Lists your AI chats")
async def aichats(ctx):
    chats = get_ai_chats(ctx.message.author.id)
    if not chats:
        await reply(ctx.message, "you have no chats")
        return
    sb = ""
    for chat_name, chat in chats.items():
        sb += chat_name + f"\n  {len(chat['messages'])} messages\n"
    await reply(ctx.message, sb)

@bot.command(help="Prompts AI in the current chat")
async def ai(ctx):
    response_text = await ask_ai(ctx.message)
    await reply(ctx.message, response_text)

@bot.command(help="Switches to or creates another AI chat")
async def aichat(ctx, arg):
    switch_ai_chat(ctx.message.author.id, arg)
    await reply(ctx.message, "switched chat to " + arg)

@bot.command(help="Resets the currently active chat")
async def aireset(ctx):
    reset_active_ai_chat(ctx.message.author.id)
    await reply(ctx.message, f"reset the {arg} chat")

@bot.command(help="Shows the messages of the currently active chat")
async def aimessagesactive(ctx):
    user_id = ctx.message.author.id
    if user_id not in ai_chats:
        await reply(ctx.message, "you don't have any chats")
        return
    if user_id not in ai_user_active_chats:
        await reply(ctx.message, "you don't have any active chat")
        return
    active_chat_name = ai_user_active_chats[user_id]
    if active_chat_name not in ai_chats[user_id]:
        ai_chats[user_id][active_chat_name] = default_chat_preset
    messages = ai_chats[user_id][active_chat_name]["messages"]
    sb = ""
    for message in messages:
        sb += f"{message['role']}: {message['content']}\n"
    await reply(ctx.message, sb)

@bot.command(help="Shows the messages of a chat")
async def aimessages(ctx, arg):
    user_id = ctx.message.author.id
    if user_id not in ai_chats:
        await reply(ctx.message, "you don't have any chats")
        return
    if arg not in ai_chats[user_id]:
        await reply(ctx.message, "you don't have a chat with that name")
        return
    messages = ai_chats[user_id][arg]["messages"]
    sb = ""
    for message in messages:
        sb += f"{message['role']}: {message['content']}\n"
    await reply(ctx.message, sb)

def run():
    bot.run(bot_token)
