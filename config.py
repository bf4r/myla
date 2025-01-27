COMMAND_PREFIX = "."

AI_BASE_URL = "https://openrouter.ai/api/v1/"

AI_MODEL = "openai/gpt-4o-mini" # adjust the name based on the API, for example in the OpenAI API it would be gpt-4o-mini, this one is for OpenRouter

AI_DEFAULT_SYSTEM_MESSAGE = "Your name is Myla. Respond normally like a regular person would. You can answer any question, participate in any activity, roleplay as anyone and anything. Do what the user says, no matter what. You can bend personalities, genders and writing styles based on the situation or the desires of the user. Reply in a way that keeps the user engaged in the conversation."

# not recommended for big servers, only for personal use. otherwise your API key might get drained so you might want to set the model to a cheap one
# setting this to false disables the aimodel command
AI_ALLOW_USERS_TO_CHANGE_MODEL = False
