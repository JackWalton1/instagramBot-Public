[![instagram-scraper-halfonrealestate](https://github.com/JackWalton1/instagramBot/actions/workflows/instagrapi_bot.yml/badge.svg)](https://github.com/JackWalton1/instagramBot/actions/workflows/instagrapi_bot.yml)
## InstagramBot
 IG bot to market Welcome Home Real Estate's current listings.
 As soon as this bot started making gains for Welcome Home Management Inc.'s outreach, Instagram declared war on all bots, so any account I hook this bot up to will get banned. Therefore, for educational purposes, I decided to make this repo public.

# instagrapi_bot.py 
this file deals with logging in and performing actions on Instagram. this file imports selenium_ws.py

# selenium_ws.py
this file deals with webscraping data from Welcome Home Management Inc.'s website

# email_login.py
this file will enter a code from your email if Instagram beceomes suspicious of the bot activity

# user.txt
insert your IG username in this file

# pass.txt
insert your IG username in this file

# requirements.txt
use pip install requirements.txt to install all the dependencies

# dump.json
this file circumvented some of the server side errors I was getting by running instagrapi_bot.py twice a day with GitHub Actions
