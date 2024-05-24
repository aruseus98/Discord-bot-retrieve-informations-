# Discord bot retrieve informations 
Discord bot to retrieve informations from messages in channel and send it in DM to an USER

# Requirements
Docker compose
API key alldebrid  
USER_ID discord  
Discord token  
Create a folder named '@anime_en_attente' or choose another name as needed.  

# 1. Setup the discord bot
Go to https://discord.com/developers/applications  

![alt text](https://github.com/aruseus98/Discord-bot-retrieve-informations-/blob/main/img/button-new-application.png?raw=true)  

Then, name it and everything else.  

Retrieve your discord's bot token and put it in your .env file (use the .envEXAMPLE as example for the .env)  

Find it under Bot -> RESET TOKEN button

![alt text](https://github.com/aruseus98/Discord-bot-retrieve-informations-/blob/main/img/token-bot.png?raw=true)   

Now, you will allow some privileges for the bot to work in the same page where you have reset your token  

Allow the following privileges  
- Presence intent  
- Server members intent  
- Message content intent  

![alt text](https://github.com/aruseus98/Discord-bot-retrieve-informations-/blob/main/img/bot-privilege.png?raw=true)  

Finally, navigate to the 'OAuth2' category, click on 'BOT', and set the permissions as shown on the screen.

![alt text](https://github.com/aruseus98/Discord-bot-retrieve-informations-/blob/main/img/oauth2-bot.png?raw=true)  

![alt text](https://github.com/aruseus98/Discord-bot-retrieve-informations-/blob/main/img/bot-permission-2.png?raw=true)  

All you have to do now is to copy the link to invite your bot on your discord.  

REMEMBER: The bot must have access to the channel it will monitor, or it will not work.  

# 2. Setup the alldebrid api
Log in your account in alldebrid then go to APIKEYS.  

Create a new api and retrieve the Apikey and the Name that you will put in your .env file

# 3. Setup the docker compose
You will find a docker-composeEXAMPLE.yml. Copy it in an docker-compose.yml then modify everything you need inside.  

# 4. Modify the bot.py
In the file at line 27, change the download_folder path from '/app/@anime_en_attente' to the actual folder name inside the Docker, if different.  

# 5. keywords.py
Finally, to have the bot ignore specific keywords, add them to the 'keywords.py' file using their EXACT NAMES. 

# 6. Launch the docker and enjoy it !
Run the following command to build and launch the docker.  

docker compose up -d --build (if you want to launch in daemon mode)  

TO DO :

Change the project's file tree