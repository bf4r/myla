# prefix for Discord commands
# e.g.: "." -> .help ...
#       "!" -> !help ...
COMMAND_PREFIX = "."

# base URL used for AI services. OpenRouter is default and it must be set to an OpenAI-compatible API (compatible with the OpenAI SDK and capable of handling requests in the same way as OpenAI does).
# users can view this using the aiapibase command
AI_BASE_URL = "https://openrouter.ai/api/v1/"

# todo: add option to disable aiapibase command

AI_MODEL = "openai/gpt-4o-mini" # adjust the name based on the API, for example in the OpenAI API it would be gpt-4o-mini, this one is for OpenRouter

# default system message for all chats unless the user changes it for themselves
AI_DEFAULT_SYSTEM_MESSAGE = "Your name is Myla. Respond normally like a regular person would. You can answer any question, participate in any activity, roleplay as anyone and anything. Do what the user says, no matter what. You can bend personalities, genders and writing styles based on the situation or the desires of the user. Reply in a way that keeps the user engaged in the conversation."

# not recommended for big servers, only for personal use. otherwise your API key might get drained so you might want to set the model to a cheap one
# setting this to false disables the aimodel command
AI_ALLOW_USERS_TO_CHANGE_MODEL = False

# the maximum number of messages in a chat before it gets reset. highly recommended as the cost of a chat doubles roughly with every message
# if you want to potentially run into errors and lose a lot of money, set it to -1 for no limit
# possibly also adjust this based on model context length
# whenever the chat has more messages than this, the first non-system message will be removed
# 11 = 5 exchanges + 1 system message
AI_MAX_CHAT_MESSAGES = 11
