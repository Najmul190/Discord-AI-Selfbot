# 🤖 Discord-AI-Selfbot

This is a [Python](https://www.python.org)-based Discord selfbot using the `discord.py-self` library. The selfbot automatically responds to messages that mention it's trigger word using Groq API's Llama-3, one of the highest performing models, **all for completely free**. You can also add your own API key for ChatGPT functionality, but this is not required. It functions as a normal Discord bot, but on a real Discord account, allowing other people to talk to it within DMs, servers and even group chats without you needing to invite a bot or add the bot to the server - making it seem like a real user to others.

> There is always the slight risk of a ban when using selfbots, so make sure to use this selfbot on an account you don't mind losing, but the risk is incredibly low and I have used it for over a year without any issues.

### **⚠️ Important:**  
*I take no responsibility for any actions taken against your account for using these selfbots or how users use my open-source code.*


<strong>Using this on a user account is prohibited by the [Discord TOS](https://discord.com/terms) and can lead to your account getting banned in _very_ rare cases.</strong>

Project made by: 

<img style="vertical-align: center;" src="https://discord.c99.nl/widget/theme-4/451627446941515817.png"/>

# 🔗 Support + Try out the bot!

If you have any questions or need assistance, please join our dedicated Discord server. You can ask your questions there and leave once you have the help you need, or stay and be part of the community!

You can also try out this project in this server, in the [#italiano](https://discord.com/channels/1269313927150309491/1270821127001866311) channel! Click the image below to join.

[![Discord Banner 2](https://discord.com/api/guilds/1269313927150309491/widget.png?style=banner2)](https://discord.gg/yUWmzQBV4P)

## 📸 Preview of Text Responses
![Example 1](https://i.imgur.com/MdfzY9C.png)

![Example 2](https://i.imgur.com/AMnx8a9.png)

## 📸 Preview of Analyse command:

![image](https://i.imgur.com/rn4Ru09.png)

> Note: This analysis is based on the user's message history and is not 100% accurate. It is just for fun and should not be taken seriously.

# ✨ Features

-   [x] Discord Selfbot: Runs on a genuine Discord account, allowing you to use it without even needing to invite a bot.
-   [x] Custom AI Instructions: You can replace the text inside of `instructions.txt` and make the AI act however you'd like!
-   [x] Free LLM Model: Enjoy the powerful capabilities of this language model without spending a dime.
-   [x] Mention Recognition: The bot only responds when you mention it or say its name.
-   [x] Reply Recognition: If replied to, the bot will continue to reply to you. It's like having a conversation with a real person!
-   [x] Message Handling: The bot knows when you're replying to someone else, so it won't cause confusion. It's like having a mind reader in your server; It can also handle numerous messages at once!
-   [x] Channel-Specific Responses: Use the `~toggleactive` command to pick what channel the bot responds in.
-   [x] Psychoanalysis Command: Use the `~analyse` command to analyse a mentioned user's messages and find insights on their personality. It's like having a therapist in your server!
-   [x] Runs on Meta AI's Llama-3: The bot uses the Llama-3 model from Meta AI, which is one of the most powerful models available.
-   [x] Secure Credential Management: Keep your credentials secure using environment variables.
-   [x] Crafted with Care: Made with lots of love and attention to detail.

## 🤖 Commands

-   analyse [user] - Analyze a user's message history and provides a - gical profile
-   wipe - Clears history of the bot
-   ping - Shows the bot's latency
-   toggleactive [channelID] - Toggle the current channel to the list of active channels
-   toggledm - Toggle if the bot should be active in DM's or not
-   togglegc - Toggle if the bot should be active in group chats or not
-   ignore [user] - Stop a user from using the bot
-   reload - Reloads all cogs
-   restart - Restarts the entire bot

# ⭐ Getting Started:

### Step 1: Download the Selfbot
- Go to the [Releases](https://github.com/Najmul190/Discord-AI-Selfbot/releases/tag/v1.0.0) page and download the latest release for your operating system.

### Step 2: Extract the files
- Extract the files to a folder of your choice, using 7Zip or Windows Explorer.

### Step 3: Getting your Discord token

-   Go to [Discord](https://canary.discord.com) and login to the account you want the token of
-   Press `Ctrl + Shift + I` (If you are on Windows) or `Cmd + Opt + I` (If you are on a Mac).
-   Go to the `Network` tab
-   Type a message in any chat, or change server
-   Find one of the following headers: `"messages?limit=50"`, `"science"` or `"preview"` under `"Name"` and click on it
-   Scroll down until you find `"Authorization"` under `"Request Headers"`
-   Copy the value which is your token


### Step 4: Getting a Groq API key

-   Go to [Groq](https://console.groq.com/keys) and sign up for a free account
-   Get your API key, which should look like `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` (this is an example key, it isn't real)

### Step 5: Running the bot

- Simply run "Discord AI Selfbot.exe" and follow the instructions in the console to set up the bot.


# 🛠️ Setting up the bot manually:

If you want to set up the bot manually because you don't trust the executable or want to edit the code yourself, follow the instructions below:

### Step 1: Git clone repository

```
git clone https://github.com/najmul190/Discord-AI-Selfbot
```

### Step 2: Changing directory to cloned directory

```
cd Discord-AI-Selfbot
```

### Step 3: Getting your Discord token

-   Go to [Discord](https://canary.discord.com) and login to the account you want the token of
-   Press `Ctrl + Shift + I` (If you are on Windows) or `Cmd + Opt + I` (If you are on a Mac).
-   Go to the `Network` tab
-   Type a message in any chat, or change server
-   Find one of the following headers: `"messages?limit=50"`, `"science"` or `"preview"` under `"Name"` and click on it
-   Scroll down until you find `"Authorization"` under `"Request Headers"`
-   Copy the value which is your token

### Step 4: Getting a Groq API key

-   Go to [Groq](https://console.groq.com/keys) and sign up for a free account
-   Get your API key, which should look like `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` (this is an example key, it isn't real)

### Step 5: Install all the dependencies and run the bot

Windows:

-   Simply open `run.bat` if you're on Windows. This will install all pre-requisites, guide you through the process of setting up the bot and run it for you.

-   If `run.bat` doesn't work, then open CMD and run `cd Discord-AI-Selfbot` to change directory to the bot files directory
-   Create a virtual environment by running `python -m venv bot-env`
-   Activate the virtual environment by running `bot-env\Scripts\activate.bat`
-   Run `pip install -r requirements.txt` to install all the dependencies
-   Fill out example.env with your own credentials and rename it to .env
-   Run the bot using `python3 main.py`

Linux:

-   If you're on Linux, then run `cd the\bot\files\directory` to change directory to the bot files directory
-   Create a virtual environment by running `python3 -m venv bot-env`
-   Activate the virtual environment by running `source bot-env/bin/activate`
-   Run `pip install -r requirements.txt` to install all the dependencies
-   Fill out example.env with your own credentials and rename it to .env
-   Run the bot using `python3 main.py`

# 🗨️ How to talk to the bot

-   To activate it in a channel use **~toggleactive channelid** (channelid is optional) or manually add the channel ID in `channels.txt`
-   To see all commands use **~help**
-   Bear in mind that the bot will only respond to **other accounts** and not itself, including any commands.
-   You must also set a trigger word within the `.env`, this is the word that the bot will respond to. For example, if you set the trigger word to `John`, people must say "Hey `John`, how are you today?" for the bot to respond.


# 💭 Changing the Personality of the bot

To change the personality of the bot and set custom instructions, simply go into the `config` folder and edit the default instructions in `instructions.txt` to whatever you want! 

# ❤️ Donate

If you appreciate this project and want to support its development, feel free to donate by clicking this button!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E1Q7XEZ)
