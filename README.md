# Discord-AI-Selfbot

This is a [Python](https://www.python.org)-based Discord selfbot using the `discord.py-self` library. The selfbot automatically responds to messages that uses it's trigger word using either ChatGPT or BARD and has image generation using an external endpoint, **all for completely free**. It functions as a normal Discord bot, just on a real Discord account, allowing other people to talk to it within DMs, servers and even group chats without you needing to invite a bot or add the bot to the server - making it seem like a real user to others.

This bot was originally [Discord-AI-Chatbot](https://github.com/mishalhossin/Discord-Chatbot-Gpt4Free/) by [MishalHossin](https://github.com/mishalhossin/) but was heavily edited by [Najmul190](https://github.com/najmul190) to work as a selfbot rather than a Discord bot.

### <strong> I take no responsibility for any actions taken against your account for using these selfbots, or how users use my open source code.</strong>

### <strong>Using this on a user account is prohibited by the [Discord TOS](https://discord.com/terms) and can lead to your account getting banned in very rare cases.</strong>

<p float="left">
  <img style="vertical-align: top;" src="https://discord.c99.nl/widget/theme-4/451627446941515817.png"/>
  <img src="https://lanyard.cnrad.dev/api/1025245410224263258?theme=dark&bg=171515&borderRadius=5px&animated=true&idleMessage=15%20year%20old%20solo%20dev" al/> 
</p>

# Preview of image responses:

![image](https://user-images.githubusercontent.com/91066601/236717834-e3f6939f-3641-425c-b9f7-424a38f86ac4.png)

# Preview of text responses:

![image](https://cdn.discordapp.com/attachments/685944147638485062/1107081044219408444/image.png)

# Preview of Image Generation:

![image](https://media.discordapp.net/attachments/715284506289897513/1113931350039343104/image.png?width=748&height=391)

# Features

- [x] Discord Selfbot: Runs on a genuine Discord account, allowing you to use it without even needing to invite a bot.
- [x] Free LLM Model: Enjoy the powerful capabilities of this language model without spending a dime.
- [x] Mention Recognition: The bot always responds when you mention it or say its name.
- [x] Reply Recognition: If replied to, the bot will continue to reply to you. It's like having a conversation with a real person!
- [x] Message Handling: The bot knows when you're replying to someone else, so it won't cause confusion. It's like having a mind reader in your server; It can also handle numerous messages at once!
- [x] Channel-Specific Responses: Use the `~toggleactive` command to pick what channel the bot responds in.
- [x] Psychoanalysis Command: Use the `~analyse` command to analyse a mentioned user's messages and find insights on their personality. It's like having a therapist in your server!
- [x] GPT-3.5-Turbo Model: This bot runs on turbo power! Powered by the lightning-fast GPT-3.5-Turbo language model.
- [x] Image Generation: Use the `~imagine` command to generate an ima-rom a prompt using AI.
- [x] BARD Model: Select the BARD model to start using Google's own model, which has up-to-date information and is more accurate, but cannot hold a conversation as well as ChatGPT or follow instructions.
- [x] Secure Credential Management: Keep your credentials secure using environment variables.
- [x] Crafted with Care: Made with lots of love and attention to detail.

## Commands

- ~model [BARD / GPT] - Change the model the bot uses to generate responses
- ~wipe - Clears history of the bot
- ~ping - Shows the bot's latency
- ~toggleactive [channel] - Toggle the current channel to the list of active channels
- ~toggledm - Toggle if the bot should be active in DM's or not
  ~ togglegc - Toggle if the bot should be active in group chats or not
- ~ignore @user - Ignore a user from using the bot
- ~imagine [prompt] - Generate an image from a prompt
- ~styles - List all the styles available for image generation
- ~analyse @user - Analyse a user's messages to provide a personality profile

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

- Go to [Discord](https://canary.discord.com) and login to the account you want the token of
- Press `Ctrl + Shift + I` (If you are on Windows) or `Cmd + Opt + I` (If you are on a Mac).
- Go to the `Network` tab
- Type a message in any chat, or change server
- Find one of the following headers: `"messages?limit=50"`, `"science"` or `"preview"` under `"Name"` and click on it
- Scroll down until you find `"Authorization"` under `"Request Headers"`
- Copy the value which is yor token

### Step 4: Get your BARD cookie value

- Go to [Google's BARD website](https://bard.google.com)
- Click `Sign in` or `Try it`
- Press `Ctrl + Shift + I` (If you are on Windows) or `Cmd + Opt + I` (If you are on a Mac).
- Go to the `Application` tab
- Click on `Cookies` under `Storage` on the left side
- Click on `https://bard.google.com` under `Cookies`
- Copy the value of `__Secure-1PSID` and paste it in the `.env` file under `BARD_COOKIE`

![image](https://media.discordapp.net/attachments/918997350238797855/1129414138347651122/image.png?width=481&height=357)

### Step 5: Rename `example.env` to `.env` and put the discord token and BARD cookie. It'll look like this:

```
BARD_COOKIE=BARD_COOKIE_GOES_HERE
DISCORD_TOKEN=DISCORD_TOKEN_GOES_HERE
OWNER_ID=OWNER_ID_GOES_HERE
SELFBOT_ID=ACCOUNT_ID_GOES_HERE
TRIGGER=TRIGGER_WORD
PREFIX=~
```

### Step 6: Install all the dependencies and run the bot

Windows:

- Simply open `run.bat` if you're on Windows. This will install all pre-requisites and run the bot as well.

- If `run.bat` doesn't work, then run `cd the\bot\files\directory` to change directory to the bot files directory
- Create a virtual environment by running `python -m venv bot-env`
- Activate the virtual environment by running `bot-env\Scripts\activate.bat`
- Run `pip install -r requirements.txt` to install all the dependencies
- Install discord.py-self using `pip install -U discord.py-self`
- Run the bot using `python3 main.py`

Linux:

- If you're on Linux, then run `cd the\bot\files\directory` to change directory to the bot files directory
- Create a virtual environment by running `python3 -m venv bot-env`
- Activate the virtual environment by running `source bot-env/bin/activate`
- Run `pip install -r requirements.txt` to install all the dependencies
- Install discord.py-self using `pip install -U discord.py-self`
- Run the bot using `python3 main.py`

# How to run on Mobile + Keep online 24/7

[![Run on repl.it](https://media.discordapp.net/attachments/1119017121960185916/1121144333047967904/image.png)](https://repl.it/github/Najmul190/Discord-AI-Selfbot)

- Click on the button above to create an account and run the bot on repl.it
- Click on `Import from GitHub`
  ![image](https://media.discordapp.net/attachments/918997350238797855/1109812776857255996/image.png?width=651&height=321)
- Do Step 3 and 4 from above to get the information
- Add the following as a secret each, along with the corresponding value: (trigger value should not be in quotes)

```
BARD_COOKIE
DISCORD_TOKEN
OWNER_ID
SELFBOT_ID
TRIGGER
PREFIX
```

![image](https://cdn.discordapp.com/attachments/918997350238797855/1129708379208691803/image.png)

- Then click on the `Run` button, which will start to install all dependencies and then run your selfbot.
- Start talking to your new friend!

# How to talk to the bot

- To activate it in a channel use **~toggleactive** in the channel or manually add the channel ID in `channels.txt`
- To see all commands use **~help**
- Bear in mind that the bot will only respond to **other accounts** and not itself, including any commands.
- You must also set a trigger word within the `.env`, this is the word that the bot will respond to. For example, if you set the trigger word to `John`, people must say "Hey `John`, how are you today?" for the bot to respond.
