# this file will use os commands to setup the install dependencies and then run main.py (used for repl.it hosting)

import os

# install dependencies
os.system("pip uninstall discord -y")
os.system("pip uninstall discord.py -y")
os.system("pip install -r requirements.txt")
os.system("pip install -U discord.py-self")

# run main.py

os.system("python3 main.py")

print("Finished installing dependencies.")
print("Make sure to fill out the bot secrets.")
