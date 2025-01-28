# prefix for Discord commands
# e.g.: "." -> .help ...
#       "!" -> !help ...
COMMAND_PREFIX = "."

# base URL used for AI services. OpenRouter is default and it must be set to an OpenAI-compatible API (compatible with the OpenAI SDK and capable of handling requests in the same way as OpenAI does).
# users can view this using the aiapibase command
AI_BASE_URL = "https://openrouter.ai/api/v1/"

# if this is set to false, the aiapibase command gets disabled. the command shows the AI base url to anyone who wants to see it.
# useful if you have a private API and don't want to reveal its link.
AI_ALLOW_APIBASE_REVEAL = True

AI_MODEL = "openai/gpt-4o-mini" # adjust the name based on the API, for example in the OpenAI API it would be gpt-4o-mini, this one is for OpenRouter

# default system message for all chats unless the user changes it for themselves
# find presets in system_msg_presets.py and set this to the name of the preset you want to use
AI_DEFAULT_SYSTEM_MESSAGE_PRESET = "myla"

# not recommended for big servers, only for personal use. otherwise your API key might get drained so you might want to set the model to a cheap one
# setting this to false disables the aimodel command
AI_ALLOW_USERS_TO_CHANGE_MODEL = False

# the maximum number of messages in a chat before it gets reset. highly recommended as the cost of a chat doubles roughly with every message
# if you want to potentially run into errors and lose a lot of money, set it to -1 for no limit
# possibly also adjust this based on model context length
# whenever the chat has more messages than this, the first non-system message will be removed
# 11 = 5 exchanges + 1 system message
AI_MAX_CHAT_MESSAGES = 11
