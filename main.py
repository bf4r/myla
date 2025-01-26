import discord
import os
from openai import OpenAI

# config
COMMAND_PREFIX = "."
AI_BASE_URL = "https://openrouter.ai/api/v1/"
AI_MODEL = "openai/gpt-4o-mini" # adjust the name based on the API, for example in the OpenAI API it would be gpt-4o-mini, this one is for OpenRouter

# setup
bot_token = os.environ["MYLA_BOT_TOKEN"]
ai_api_key = os.environ["AI_API_KEY"]

ai_client = OpenAI(
    api_key=ai_api_key,
    base_url=AI_BASE_URL
)

def iscmd(msg, cmdstr):
    return msg.content.startswith(COMMAND_PREFIX + cmdstr);

async def ask_ai(msg):
    prompt = msg.content[3:].strip() # remove ".ai "
    completion = ai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=AI_MODEL,
    )
    return completion.choices[0].message.content

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
            await msg.reply(response_text)


intents = discord.Intents.default()
intents.message_content = True

bot_client = BotClient(intents=intents)
bot_client.run(bot_token)
