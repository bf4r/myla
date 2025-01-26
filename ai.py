from openai import OpenAI
import os
from config import *

ai_api_key = os.environ.get("AI_API_KEY")
if not ai_api_key:
    print("Please set the AI_API_KEY environment variable with the key of the API you're using.\nWindows:\nset AI_API_KEY=...\nUnix-like:\nexport AI_API_KEY=...")
    exit(1)

ai_client = OpenAI(
    api_key=ai_api_key,
    base_url=AI_BASE_URL
)

ai_chats = {}

# tells which user is currently using which chat
# e.g. user1 has activated chat1
# default chat name is default
ai_user_active_chats = {}

async def ask_ai(msg):
    prompt = msg.content[3:].strip() # remove ".ai "

    user_id = msg.author.id
    if user_id not in ai_user_active_chats:
        # if the user has just started chatting for the first time, set their active chat name to default
        ai_user_active_chats[user_id] = "default"
    # check if either the user has no chats list or the active chat does not exist in their list
    # if not, create the default one
    if user_id not in ai_chats:
        ai_chats[user_id] = {}
    if ai_user_active_chats[user_id] not in ai_chats[user_id]:
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

def switch_ai_chat(msg):
    user_id = msg.author.id
    chat_name = msg.content[7:].strip() # remove ".aichat "
    ai_user_active_chats[user_id] = chat_name

def get_ai_chats(msg):
    user_id = msg.author.id
    if user_id not in ai_chats:
        return []
    return ai_chats[user_id]
