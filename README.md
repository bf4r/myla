# myla
Discord bot

## Quickstart/TLDR
It is highly recommended to read the full installation guide (Installation section below) if you don't know much about Discord bots, environment variables, don't have an OpenRouter account or want to use the OpenAI API instead.

## Quick installs
The following assume you have already set the AI_API_KEY and MYLA_BOT_TOKEN environment variables.
### Windows
```bash
winget install --id Git.Git -e --source winget
winget install -e --id Python.Python.3.12
git clone https://github.com/bf4r/myla
cd myla
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
### Linux/MacOS
Pacman is just an example here. Replace it with your actual package manager. The command for installing git and python might be different.
```
sudo pacman -S git python
git clone https://github.com/bf4r/myla
cd myla
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Installation
### 0. Install git if you don't already have it
Alternatively, you can download the ZIP file using the Code button on GitHub and clicking Download ZIP. Then extract it and go into that folder. If you do this, you can skip step 1.
```bash
# Windows
# https://git-scm.com/downloads/win

# Arch Linux
sudo pacman -S git
# or your preferred package manager or the one for your distribution

# MacOS
brew install git
```

### 1. Clone the repository
```bash
git clone https://github.com/bf4r/myla
cd myla
```
### 2. Set environment variables
#### AI API key
The default API for AI services is [OpenRouter](https://openrouter.ai). To change it, edit config.py and change AI_BASE_URL to something like https://api.openai.com/v1 for the OpenAI API. The API must be OpenAI-compatible, so it is highly suggested to use OpenRouter since it provides most models through an OpenAI-compatible API. To get an OpenRouter API key, create an OpenRouter account, [create an API key](https://openrouter.ai/settings/keys), [add some credits to your account](https://openrouter.ai/credits) and replace the ... with your own API key in the example below. If you end up using the OpenAI API instead, change the model ID in config.py (AI_MODEL) to not have the "openai/" prefix that OpenRouter uses.
#### Discord bot token
To host this bot yourself, visit the [Discord developer portal](https://discord.com/developers/applications) and create an application. Click on your application, then click on the Bot section in the sidebar, click on the "Reset Token" button and copy the token. Keep it somewhere secure and replace the ... after MYLA_BOT_TOKEN when your newly created bot token. To invite the bot to your server, click on the OAuth2 section in the sidebar, scroll down to the OAuth2 URL Generator, check the checkbox next to "bot", select your desired permissions for the bot (if you're unsure, select "Send Messages" and any other permissions you want the bot to have and if you don't care, select "Administrator"), then scroll down and copy the generated URL link. Go to that link and select a server to add the bot to.
```bash
# Windows
set AI_API_KEY=...
set MYLA_BOT_TOKEN=...

# Linux/MacOS
export AI_API_KEY=...
export MYLA_BOT_TOKEN=...
```
### 3. Install Python 3.12+
Link: https://www.python.org/downloads
```bash
# Arch Linux
sudo pacman -S python
# for other distros, replace the package manager or look up how to install Python
```
### 4. Create a virtual Python environment to install packages in an isolated way
```bash
python -m venv venv
```
...and activate it using the activation script:
```bash
# Windows
venv\Scripts\activate

# Linux/MacOS
source venv/bin/activate
```
### 5. Install the required Python packages
```bash
pip install -r requirements.txt
```
### 6. Start the bot
```bash
python main.py
```
Anytime you want to run this again, make sure you have Python, cd into the repository folder, activate the virtual environment and do `python main.py`.

## Configuration
Open the config.py file (in the root directory of the project) and read the comments to learn more about the configuration options. Edit them as you'd like. The configuration already contains sensible defaults, however most people don't have an OpenRouter account, so you might want to change the API type to OpenAI. In that case, change the AI_BASE_URL to https://api.openai.com/v1/ and the AI_MODEL to something like "gpt-4o" or whatever OpenAI model you want to use (without the "openai/" prefix which is specific to OpenRouter because it's an API that provides models from multiple organizations).
