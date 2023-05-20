# Discord-AI-Selfbot

This is a [Python](https://www.python.org)-based Discord selfbot using the `discord.py-self` library. The selfbot automatically responds to messages that uses it's name using AI and can provide latency information, along with image generation using DALL-E. It uses the [OpenGPT](https://github.com/uesleibros/OpenGPT) module to generate responses based on conversation history. It functions as a normal Discord bot, just on a real Discord account, allowing other people to talk to it within DMS, servers and even group chats.

This bot was originally [Discord-Chatbot-Gpt4Free](https://github.com/mishalhossin/Discord-Chatbot-Gpt4Free/) by [MishalHossin](https://github.com/mishalhossin/) but was heavily edited by [Najmul190](https://github.com/najmul190) to work as a selfbot rather than a Discord bot.

### <strong> I take no responsibility for any actions taken against your account for using this bot.</strong>

### <strong>Using this on a user account is prohibited by the [Discord TOS](https://discord.com/terms) and can lead to your account getting banned in rare cases.</strong>

<p float="left">
  <img style="vertical-align: top;" src="https://discord.c99.nl/widget/theme-4/451627446941515817.png"/>
  <img src="https://lanyard.cnrad.dev/api/1025245410224263258?theme=dark&bg=171515&borderRadius=5px&animated=true&idleMessage=15%20year%20old%20solo%20dev" al/> 
</p>

---

# Preview of image responses:

![image](https://user-images.githubusercontent.com/91066601/236717834-e3f6939f-3641-425c-b9f7-424a38f86ac4.png)

# Preview of text responses:

![image](https://cdn.discordapp.com/attachments/685944147638485062/1107081044219408444/image.png)

# Features

- [x] Discord Selfbot: Runs on a genuine Discord account, allowing you to use it without even needing to invite a bot.
- [x] Free LLM Model: Enjoy the powerful capabilities of this language model without spending a dime.
- [x] Mention Recognition: The bot always responds when you mention it or say its name. It's as attentive as a squirrel spotting a shiny acorn!
- [x] Reply Recognition: If replied to, the bot will continue to reply to you. It's like having a conversation with a real person!
- [x] Message Handling: The bot knows when you're replying to someone else, so it won't cause confusion. It's like having a mind reader in your server; It can also handle numerous messages at once!
- [x] Channel-Specific Responses: Use the `~toggleactive` command to pick what channel the bot responds in.
- [x] GPT-3.5-Turbo Model: This bot runs on turbo power! Powered by the lightning-fast GPT-3.5-Turbo language model.
- [x] Image Detection Model: The bot can detect objects in images using a fancy Hugging Face API.
- [x] Secure Credential Management: Keep your credentials secure using environment variables.
- [x] Crafted with Care: Made with lots of love and attention to detail.

# Preview of Image Generation:

![image](https://cdn.discordapp.com/attachments/691684867271950336/1109469317986267146/image.png)

## Commands

- ~pfp [image_url] - Change the bot's profile picture
- ~wipe - Clears history of the bot
- ~ping - Shows the bot's latency
- ~toggleactive [channel] - Toggle the current channel to the list of active channels
- ~toggledm - Toggle if the bot should be active in DM's or not
- ~ignore [user] - Ignore a user from using the bot
- ~imagine [prompt] - Generate an image from a prompt

# Steps to install and run:

### Step 1: Git clone repository

```
git clone https://github.com/najmul190/DiscordGPT4FreeSelfBot
```

### Step 2: Changing directory to cloned directory

```
cd DiscordGPT4FreeSelfBot
```

### Step 3: Getting your Discord token

- Go to [Discord](https://canary.discord.com) and login to the account you want the token of
- Press `Ctrl + Shift + I` (If you are on Windows) or `Cmd + Opt + I` (If you are on a Mac).
- Go to the `Network` tab
- Type a message in any chat, or change server
- Find one of the following headers: `"messages?limit=50"`, `"science"`, `"preview"` under `"Name"` and click on it
- Scroll down until you find `"Authorization"` under `"Request Headers"`
- Copy the value

### Step 4: Get hugging face Access Tokens from [here](https://huggingface.co/settings/tokens)

- Pick either read or write, it doesn't matter

![image](https://user-images.githubusercontent.com/91066601/236681615-71600817-774a-430c-8cec-8e6710a82b49.png)

### Step 5: Rename `example.env` to `.env` and put the discord token and hugging face access token. It'll look like this:

```
HUGGING_FACE_API=API_KEY
DISCORD_TOKEN=SELFBOT_TOKEN
OWNER_ID=ID_OF_YOUR_ACCOUNT
SELFBOT_ID=ID_OF_SELFBOT_ACCOUNT
TRIGGER="TRIGGER-WORD-GOES-HERE"
```

### Step 6: Install all the dependencies and run the bot

Windows:

- Simply open `run.bat` if you're on Windows. This will install all pre-requisites and run the bot as well.

- If `run.bat` doesn't work, then run `cd the\bot\files\directory` to change directory to the bot files directory
- Create a virtual environment by running `python -m venv bot-env`
- Activate the virtual environment by running `bot-env\Scripts\activate.bat`
- Run `pip install -r requirements.txt` to install all the dependencies

Linux:

- If you're on Linux, then run `cd the\bot\files\directory` to change directory to the bot files directory
- Create a virtual environment by running `python3 -m venv bot-env`
- Activate the virtual environment by running `source bot-env/bin/activate`
- Run `pip install -r requirements.txt` to install all the dependencies
- Install discord.py-self using `pip install -U discord.py-self`
- Run the bot using `python3 main.py`

# How to run on Mobile + Keep online 24/7

# [![Run on repl.it](https://camo.githubusercontent.com/56417b1780ddc0e04d7c9ce2e4041a437a25aeaa898473a75695723e88a9d043/68747470733a2f2f7265706c2d62616467652e6a616a6f6f73616d2e7265706c2e636f2f7472792e706e67)](https://repl.it/github/Najmul190/Discord-AI-Selfbot)

### How to talk to the bot

- To activate it in a channel use **~toggleactive** in the channel or manually add the channel ID in `channels.txt`
- To see all commands use **~help**
- Bear in mind that the bot will only respond to **other accounts** and not itself, including any commands.
- You must also set a trigger word within the `.env`, this is the word that the bot will respond to. For example, if you set the trigger word to `John`, people must say "Hey `John`, how are you today?" for the bot to respond.
