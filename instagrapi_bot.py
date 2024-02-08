from instagrapi import Client
import os
import glob
import shutil
from instagrapi.mixins.challenge import ChallengeChoice

# from bot_launcher import keep_alive


## this IGbot makes sure I only post what I have not posted by the following:

### selenium_ws.py will scrape all "updated" info 
### selenium will pass on the info in Listings folder
### bot reads IG caption, then check if any of the listings in 
#### Listings folder contains the same caption:
    #if contains caption on system and not on IG: 
        # post new listing
    #if contains caption on IG and not on system: 
        # delete old listing post

#uses text file path grabbed by glob to create list of photo paths/listing
def get_photoLinksPaths(text_file_path):
    photoLinkPath = text_file_path[:-11]
    photoLinkPath+='photoLinks/'
    album_paths = sorted(os.listdir(photoLinkPath))
    i=0
    for album_path in album_paths:
        album_path=photoLinkPath+album_path
        album_paths[i] = album_path
        i+=1
    return album_paths

#this checks whether we need to add post or keep
def scrapedCaptionIsOnIG(listingCaption, posts):
    for post in posts:
        if " ".join(listingCaption.split()) == " ".join(post.caption_text.split()):
            return True; #post exists for listing
    return False #post does not exist for listing

#this checks whether we need to remove post or keep
def IGCaptionIsOnScraper(text_files_paths, post):
    for text_file in text_files_paths:
        file_contents = read_file_contents(text_file)
        if " ".join(file_contents.split()) == " ".join(post.caption_text.split()):
                return True;
    return False;

#gets all the contnets of a file (used for scraped messages)
def read_file_contents(filepath):
    IGCaptionMax = 2200
    if os.path.exists(filepath):
        f = open(filepath,  "r")
        contents = f.read()
        if (len(contents)>IGCaptionMax):
            return contents[:IGCaptionMax-1]
        else:
            return contents
    return None

def get_user_passw():
    with open('user.txt', 'r') as file:
        user = file.read().replace('\n', '')
    with open('pass.txt', 'r') as file:
        passw = file.read().replace('\n', '')
    return user, passw

def challenge_code_handler(username, choice):
    if choice == ChallengeChoice.SMS:
        print("\nNever taught how to handle this (SMS challenge)")
        return False
    elif choice == ChallengeChoice.EMAIL:
        import email_login
        if len(email_login.codes) <= 0:
            print("\nNo code found in instagrapi_bot.py")
            return False
        else:
            print("\nCode was found in instagrapi_bot.py")
            return email_login.codes[0] #returns most recent login code from instagram
    return False

def change_password_handler(username):
    password = "NEWPASS"
    return password


##import webscraping (bot scrapes every time its launched)
import selenium_ws

# ACCOUNT_USERNAME, ACCOUNT_PASSWORD = get_user_passw()
##LOGIN
bot = Client()
ACCOUNT_USERNAME, ACCOUNT_PASSWORD = get_user_passw()
bot.load_settings('./dump.json')
try: 
    # bot.dump_settings('./dump.json')
    # bot.load_settings('./dump.json')
    bot.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
except:
    bot.challenge_code_handler = challenge_code_handler
    bot.change_password_handler = change_password_handler
    bot.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
    bot.get_timeline_feed()
# bot.change_password_handler = change_password_handler

# bot.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
# except:
#     print("\nBot sleeping for 10 seconds to wait for email....")
#     # time.sleep(10)
# bot.challenge_code_handler = challenge_code_handler
# bot.change_password_handler = change_password_handler
#     bot.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

# bot.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
##GET CURRENT POSTS TO READ CAPTIONS IN
curr_posts = bot.user_medias(bot.user_id)
##CHECK IF CAPTION WAS SCRAPED FROM SITE OR NOT
scraper_path = os.getcwd()+'/Listings'
##use glob to get a list of all scraped txt files saved to system
text_files_paths = glob.glob(scraper_path + "/**/*.txt", recursive = True)
##CHECK IF SCRAPED CAPTION IS ON IG/IG CAPTION WAS EVEN SCRAPED
## loop to go through all messages saved by scraper

updated = False
for text_file_path in text_files_paths:
    caption = read_file_contents(text_file_path) ##get CAPTION for comparison
    #if scrapedCaptionIsOnIG returns false, we post the listing
    if not (scrapedCaptionIsOnIG(caption, curr_posts)):
        albumPaths = get_photoLinksPaths(text_file_path)##get PHOTOLINKS for post
        print("\nNew Post! Posting: "+text_file_path)
        bot.album_upload(paths=albumPaths, caption=caption)
        updated = True
##update current posts after posting new listings
curr_posts = bot.user_medias(bot.user_id)
##loop to go through all posts already on instagram, check if still on website
for post in curr_posts:
    ##If IGCaptionisOnScraper returns false, we remove the post
    if not (IGCaptionIsOnScraper(text_files_paths, post)):
        print("\nNew Remove!")
        stale_post_pk = post.pk
        bot.media_delete(stale_post_pk)
        updated = True
if updated:
    print("Updated.")
else:
    print("Everything is already up to date.")
#clear all listings that were scraped once all checks have been made
try:
    shutil.rmtree(scraper_path)
except OSError as e:
    print("Error: %s : %s" % (scraper_path, e.strerror))
    # user_id = bot.user_id_from_username("jackwwalton")
    # bot.direct_send("Hello broh\nHow u doin'", user_ids=[user_id])


    # album_paths = get_photoLinksPaths()
    # caption = selenium_ws.first_caption
    # bot.album_upload(
    #         album_paths,
    #         caption
    #     )

