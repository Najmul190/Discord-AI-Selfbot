# Discord-AI-Selfbot

This is a [Python](https://www.python.org)-based Discord selfbot using the `discord.py-self` library. The selfbot automatically responds to messages that mention it's trigger word using Groq API's Llama-3, one of the highest performing models, **all for completely free**. It functions as a normal Discord bot, but on a real Discord account, allowing other people to talk to it within DMs, servers and even group chats without you needing to invite a bot or add the bot to the server - making it seem like a real user to others.

> There is always the slight risk of a ban so make sure to use this selfbot on an account you don't mind losing, but the risk is incredibly low and I have used it for over a year without any issues.

This bot was originally [Discord-AI-Chatbot](https://github.com/mishalhossin/Discord-AI-Chatbot) by [MishalHossin](https://github.com/mishalhossin/) but was heavily edited by [Najmul190](https://github.com/najmul190) to work as a selfbot rather than a Discord bot.

### <strong> I take no responsibility for any actions taken against your account for using these selfbots, or how users use my open source code.</strong>

### <strong>Using this on a user account is prohibited by the [Discord TOS](https://discord.com/terms) and can lead to your account getting banned in _very_ rare cases.</strong>

<p float="left">
  <img style="vertical-align: top;" src="https://discord.c99.nl/widget/theme-4/451627446941515817.png"/>
  <img src="https://lanyard.cnrad.dev/api/1025245410224263258?theme=dark&bg=171515&borderRadius=5px&animated=true&idleMessage=15%20year%20old%20solo%20dev" al/> 
</p>

# Preview of text responses:

![image](https://cdn.discordapp.com/attachments/1241152501336772709/1267566207247188079/image.png?ex=66a94086&is=66a7ef06&hm=11cac192c2a18be7c3154a6154e841c6adffb64ff577a3f78e961b3055f00b50&)

![image](https://cdn.discordapp.com/attachments/1241152501336772709/1267566298200543232/image.png?ex=66a9409b&is=66a7ef1b&hm=b1396a8be36f87399bd23f450876a176f916ca25880a8e2931ecceaf1e912af3&)

# Preview of Analyse command:

![image](https://media.discordapp.net/attachments/1241152501336772709/1267572436925284414/image.png?ex=66a94653&is=66a7f4d3&hm=49c85bf2dae7cda83c6cf4573b65da67cc78b00fcbc683cab8ebb8c78a1cb42b&=&format=webp&quality=lossless&width=614&height=326)

> Note: This analysis is based on the user's message history and is not 100% accurate. It is just for fun and should not be taken seriously.

# Features

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

## Commands

-   analyse [user] - Analyze a user's message history and provides a - gical profile
-   wipe - Clears history of the bot
-   ping - Shows the bot's latency
-   toggleactive - Toggle the current channel to the list of active channels
-   toggledm - Toggle if the bot should be active in DM's or not
-   togglegc - Toggle if the bot should be active in group chats or not
-   ignore [user] - Stop a user from using the bot
-   reload - Reloads all cogs
-   restart - Restarts the entire bot

# Steps to install and run:

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
-   Copy the value which is yor token

### Step 4: Getting a Groq API key

-   Go to [Groq](https://console.groq.com/keys) and sign up for a free account
-   Get your API key, which should look like `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` (this is an example key, it isn't real)

### Step 5: Rename `example.env` to `.env` and put your Discord token and Groq API key in. It'll look like this:

```
DISCORD_TOKEN=TOKEN_GOES_HERE
GROQ_API_KEY=GROQ_API_KEY_GOES_HERE
OWNER_ID=ID_OF_YOUR_MAIN_DISCORD_ACCOUNT
TRIGGER=WORD_YOU_WANT_TO_TRIGGER_BOT_WITH
PREFIX=~
```

> The `OWNER_ID` is the ID of your main Discord account, which will be the only account allowed to use important commands, such as toggleactive, wipe, etc.

### Step 6: Install all the dependencies and run the bot

Windows:

-   Simply open `run.bat` if you're on Windows. This will install all pre-requisites and run the bot as well.

-   If `run.bat` doesn't work, then open CMD and run `cd Discord-AI-Selfbot` to change directory to the bot files directory
-   Create a virtual environment by running `python -m venv bot-env`
-   Activate the virtual environment by running `bot-env\Scripts\activate.bat`
-   Run `pip install -r requirements.txt` to install all the dependencies
-   Install discord.py-self using `pip install -U discord.py-self`
-   Run the bot using `python3 main.py`

Linux:

-   If you're on Linux, then run `cd the\bot\files\directory` to change directory to the bot files directory
-   Create a virtual environment by running `python3 -m venv bot-env`
-   Activate the virtual environment by running `source bot-env/bin/activate`
-   Run `pip install -r requirements.txt` to install all the dependencies
-   Install discord.py-self using `pip install -U discord.py-self`
-   Run the bot using `python3 main.py`

# How to talk to the bot

-   To activate it in a channel use **~toggleactive** in the channel or manually add the channel ID in `channels.txt`
-   To see all commands use **~help**
-   Bear in mind that the bot will only respond to **other accounts** and not itself, including any commands.
-   You must also set a trigger word within the `.env`, this is the word that the bot will respond to. For example, if you set the trigger word to `John`, people must say "Hey `John`, how are you today?" for the bot to respond.

# Donate

If you're feeling rich and grateful, feel free to donate by clicking this button!

[![ko-fi](https://www.ko-fi.com/img/donate_sm.png)](https://ko-fi.com/najmulx)
