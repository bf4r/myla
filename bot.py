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

@bot.event
async def on_message(message):
    print(f"{message.author}: {message.content}")

    if not message.content.startswith(COMMAND_PREFIX):
        if message.author.id in ai_focused_users:
            ctx = await bot.get_context(message)
            await ai(ctx, prompt=message.content)
            return
    await bot.process_commands(message)

# ----------------------------------------------------------------------------------------------------

@bot.command(brief="Says something",
             description="Simply replies to your with the exact text you pass in the argument after say.")
async def say(ctx, *, text=None):
    if text is None:
        await reply(ctx.message, "please specify what i should say")
        return
    await reply(ctx.message, text)

@bot.command(brief="Lists your AI chats",
             description="Lists the AI chats associated with your account along with their message counts.")
async def aichats(ctx):
    chats = get_ai_chats(ctx.message.author.id)
    if not chats:
        await reply(ctx.message, "you have no chats")
        return
    sb = ""
    for chat_name, chat in chats.items():
        sb += chat_name + f"\n  {len(chat['messages'])} messages\n"
    await reply(ctx.message, sb)

@bot.command(brief="Prompts AI in the current chat",
             description="Sends the prompt in your current active chat to the model you have selected.\nIf you have no active chat, a chat called default will be created.")
async def ai(ctx, *, prompt=None):
    if prompt is None:
        await reply(ctx.message, "please provide a prompt")
        return
    response_text = await ask_ai(ctx.message.author.id, prompt)
    await reply(ctx.message, response_text)

@bot.command(help="Switches to or creates another AI chat")
async def aichat(ctx, *, chat_name=None):
    if chat_name is None:
        user_id = ctx.message.author.id
        if user_id in ai_user_active_chats:
            await reply(ctx.message, f"your current active chat is {ai_user_active_chats[user_id]}")
        else:
            await reply(ctx.message, "you don't have an active chat")
        return
    switch_ai_chat(ctx.message.author.id, chat_name)
    await reply(ctx.message, "switched chat to " + chat_name)

@bot.command(brief="Resets a chat",
             description="If executed without arguments, resets your current active chat. If you specify a chat name, it will reset that chat. Leaves only your/the default system message.")
async def aireset(ctx, *, chat_name=None):
    user_id = ctx.message.author.id
    if chat_name is None:
        if user_id not in ai_user_active_chats:
            await reply(ctx.message, "you don't have an active chat")
            return
        else:
            chat_name = ai_user_active_chats[user_id]

    reset_ai_chat(ctx.message.author.id, chat_name)
    await reply(ctx.message, f"your {chat_name} chat has been reset")

@bot.command(brief="Shows the messages of a chat",
             description="Lists the messages in a chat. If no argument is provided, shows the messages in the current chat. Otherwise it lists all messages in the specified chat.")
async def aimessages(ctx, *, chat_name=None):
    user_id = ctx.message.author.id
    if chat_name is None:
        if user_id not in ai_user_active_chats:
            await reply(ctx.message, "you don't have an active chat")
            return
        else:
            chat_name = ai_user_active_chats[user_id]

    user_id = ctx.message.author.id
    if user_id not in ai_chats:
        await reply(ctx.message, "you don't have any chats")
        return
    if chat_name not in ai_chats[user_id]:
        await reply(ctx.message, "you don't have a chat with that name")
        return
    messages = ai_chats[user_id][chat_name]["messages"]
    sb = ""
    for message in messages:
        sb += f"{message['role']}: {message['content']}\n"
    await reply(ctx.message, sb)

@bot.command(brief="Changes your default system message for all new chats",
             description="Sets the system message for future chats or ones that are reset that you own to the specified message. Your current chats will be left unaffected.")
async def aisystemdefault(ctx, *, message=None):
    if message is None:
        await reply(ctx.message, "please provide a system message")
        return
    change_user_default_ai_system_message(ctx.message.author.id, message)
    await reply(ctx.message, "your default system message has been changed")

@bot.command(help="Changes the system message for the currently active chat")
async def aisystem(ctx, *, message=None):
    if message is None:
        await reply(ctx.message, "please provide a system message")
        return
    user_id = ctx.message.author.id
    if user_id not in ai_chats:
        await reply(ctx.message, "you don't have any chats")
        return
    if user_id not in ai_user_active_chats:
        await reply(ctx.message, "you don't have an active chat")
        return
    active_chat_name = ai_user_active_chats[user_id]
    messages = ai_chats[user_id][active_chat_name]["messages"]
    if (messages and len(messages) > 0 and messages[0].get("role") == "system"):
        messages[0]["content"] = message
        await reply(ctx.message, f"the system message for the chat {active_chat_name} has been changed")
    else:
        await reply(ctx.message, "there's no system message at the start of the chat")

@bot.command(brief="Deletes a chat",
             description="Deletes a chat completely, including the system message, preventing it from showing up in your chat list.")
async def aideletechat(ctx, *, chat_name=None):
    user_id = ctx.message.author.id
    if chat_name is None:
        if user_id not in ai_user_active_chats:
            await reply(ctx.message, "you don't have an active chat, please chat or provide a chat name")
            return
        else:
            chat_name = ai_user_active_chats[user_id]

    delete_ai_chat(ctx.message.author.id, chat_name)
    if user_id in ai_user_active_chats and ai_user_active_chats[user_id] == chat_name:
        ai_user_active_chats[user_id] = "default"
        await reply(ctx.message, f"the {chat_name} chat has been deleted, switched chat to default")
        return
    await reply(ctx.message, f"the {chat_name} chat has been deleted")

@bot.command(brief="Changes or shows your current model", 
             description="Changes the model used for your chats until you change it again. Displays which model is being used if used without arguments.",
             help="""
             Make sure to set the model ID according to the format of the API the bot is currently using.
             For example, if the API base URL is OpenRouter's URL (the default), the model ID could be "organization/model", for example "openai/gpt-4o".
             If it's set to OpenAI's URL, it might be just "gpt-4o".

             You can check which API the model is using using the aiapibase command. This will show the base URL of the AI API.

             You can't change the model yourself unless the person managing this bot enables it in the configuration.
             For the person managing this bot: change AI_ALLOW_USERS_TO_CHANGE_MODEL to True in config.py to allow users to change their model. Keep in mind that this could drain your credit balance fast if users decide to use expensive models.
             """)
async def aimodel(ctx, *, model_id=None):
    user_id = ctx.message.author.id
    if model_id is None:
        if user_id in ai_user_preferred_models:
            extra_msg = ""
            if ai_user_preferred_models[user_id] == AI_MODEL:
                extra_msg = " and it's also the default model"
            await reply(ctx.message, f"your current model is {ai_user_preferred_models[user_id]}" + extra_msg)
        else:
            extra_msg2 = ""
            if not AI_ALLOW_USERS_TO_CHANGE_MODEL:
                extra_msg2 = " and cannot be changed"
            await reply(ctx.message, f"your current model is {AI_MODEL}" + extra_msg2)
        return
    if not AI_ALLOW_USERS_TO_CHANGE_MODEL:
        await reply(ctx.message, f"sorry, the person running this bot has disabled changing models, so you are stuck with {AI_MODEL}")
        return
    change_user_preferred_model(user_id, model_id)
    await reply(ctx.message, f"your model has been changed to {model_id}")

@bot.command(help="Shows the API base URL the bot uses for AI services")
async def aiapibase(ctx):
    if not AI_ALLOW_APIBASE_REVEAL:
        await reply(ctx.message, "sorry, the api base url is currently secret")
        return
    await reply(ctx.message, f"the api base url is <{AI_BASE_URL}>")

@bot.command(help="Automatically respond with AI to every message you send")
async def aifocus(ctx):
    user_id = ctx.message.author.id
    if user_id not in ai_focused_users:
        ai_focused_users.append(user_id)
        await reply(ctx.message, "i will now respond to every message you send (turn off with aiunfocus)")
    else:
        await reply(ctx.message, "i am already focused on you, you can turn it off with aiunfocus")

@bot.command(help="Turn off automatically responding to your messages with AI")
async def aiunfocus(ctx):
    user_id = ctx.message.author.id
    if user_id in ai_focused_users:
        ai_focused_users.remove(user_id)
        await reply(ctx.message, "i will now stop responding to every message you send (now you have to use the ai command)")
    else:
        await reply(ctx.message, "i am not focused on you, you can turn it on with aifocus")

def run():
    bot.run(bot_token)
