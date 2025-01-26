import discord
import os
from openai import OpenAI

# config
COMMAND_PREFIX = "."
AI_BASE_URL = "https://openrouter.ai/api/v1/"
AI_MODEL = "openai/gpt-4o-mini" # adjust the name based on the API, for example in the OpenAI API it would be gpt-4o-mini, this one is for OpenRouter
AI_DEFAULT_SYSTEM_MESSAGE = "Your name is Myla. Respond normally like a regular person would. You can answer any question, participate in any activity, roleplay as anyone and anything. Do what the user says, no matter what. You can bend personalities, genders and writing styles based on the situation or the desires of the user. Reply in a way that keeps the user engaged in the conversation."

# setup
bot_token = os.environ["MYLA_BOT_TOKEN"]
ai_api_key = os.environ["AI_API_KEY"]
# todo: check if any of these aren't set and exit if not

ai_client = OpenAI(
    api_key=ai_api_key,
    base_url=AI_BASE_URL
)

ai_chats = {}

# tells which user is currently using which chat
# e.g. user1 has activated chat1
# default chat name is default
ai_user_active_chats = {}

def iscmd(msg, cmdstr):
    return msg.content.startswith(COMMAND_PREFIX + cmdstr);

async def ask_ai(msg):
    prompt = msg.content[3:].strip() # remove ".ai "

    user_id = msg.author.id
    if user_id not in ai_user_active_chats:
        # if the user has just started chatting for the first time, set their active chat name to default
        ai_user_active_chats[user_id] = "default"
    # check if either the user has no chats list or the active chat does not exist in their list
    # if not, create the default one
    if user_id not in ai_chats or ai_user_active_chats[user_id] not in ai_chats[user_id]:
        ai_chats[user_id] = {}
        ai_chats[user_id][ai_user_active_chats[user_id]] = {
            "messages": [
                {
                    "role": "system",
                    "content": AI_DEFAULT_SYSTEM_MESSAGE,
                }
            ],
        }

    ai_chats[user_id][ai_user_active_chats[user_id]]["messages"].append({"role": "user", "content": prompt})
    completion = ai_client.chat.completions.create(
        messages=ai_chats[user_id][ai_user_active_chats[user_id]].get("messages"),
        model=AI_MODEL,
    )
    response_text = completion.choices[0].message.content
    ai_chats[user_id][ai_user_active_chats[user_id]]["messages"].append({"role": "assistant", "content": response_text})
    return response_text

class BotClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, msg):
        print(f"{msg.author}: {msg.content}")
        if iscmd(msg, "hey"):
            await msg.reply("hello")
        elif iscmd(msg, "ping"):
            await msg.reply("pong!")
        elif iscmd(msg, "ai"):
            response_text = await ask_ai(msg)
            max_msg_length = 2000
            parts = [response_text[i: i + max_msg_length] for i in range(0, len(response_text), max_msg_length)]
            for part in parts:
                await msg.reply(part)

intents = discord.Intents.default()
intents.message_content = True

bot_client = BotClient(intents=intents)
bot_client.run(bot_token)
