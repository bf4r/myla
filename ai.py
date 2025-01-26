from openai import OpenAI
import os
from config import *
import copy

ai_api_key = os.environ.get("AI_API_KEY")
if not ai_api_key:
    print("Please set the AI_API_KEY environment variable with the key of the API you're using.\nWindows:\nset AI_API_KEY=...\nUnix-like:\nexport AI_API_KEY=...")
    exit(1)

ai_client = OpenAI(
    api_key=ai_api_key,
    base_url=AI_BASE_URL
)

ai_chats = {}

default_chat_preset = {
            "messages": [
                {
                    "role": "system",
                    "content": AI_DEFAULT_SYSTEM_MESSAGE,
                }
            ],
        }

# tells which user is currently using which chat
# e.g. user1 has activated chat1
# default chat name is default
ai_user_active_chats = {}

async def ask_ai(msg):
    prompt = msg.content[3:].strip() # remove ".ai "

    user_id = msg.author.id
    if user_id not in ai_user_active_chats:
        ai_user_active_chats[user_id] = "default"

    active_chat = ai_user_active_chats[user_id]

    # check if the user has a chats list, and if not, create it
    if user_id not in ai_chats:
        ai_chats[user_id] = {}

    # check if the user has the active chat in the chats list, and if not, create it
    if active_chat not in ai_chats[user_id]:
        ai_chats[user_id][active_chat] = copy.deepcopy(default_chat_preset)

    # add the user message to the chat
    ai_chats[user_id][active_chat]["messages"].append({"role": "user", "content": prompt})
    # make the request
    completion = ai_client.chat.completions.create(
        messages=ai_chats[user_id][active_chat].get("messages"),
        model=AI_MODEL,
    )
    response_text = completion.choices[0].message.content
    # add the ai message to the chat
    ai_chats[user_id][active_chat]["messages"].append({"role": "assistant", "content": response_text})
    return response_text

def switch_ai_chat(user_id, chat_name):
    ai_user_active_chats[user_id] = chat_name

def get_ai_chats(user_id):
    if user_id not in ai_chats:
        return []
    return ai_chats[user_id]

def reset_active_ai_chat(user_id):
    if user_id in ai_chats:
        ai_chats[user_id][ai_user_active_chats[user_id]] = copy.deepcopy(default_chat_preset)
