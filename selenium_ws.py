from selenium import webdriver
from selenium import webdriver
# from pyvirtualdisplay import Display
import chromedriver_autoinstaller

import bs4 
import requests
import os

#this class just makes things a little neater to debug
class Listing:
    def __init__(self, photoLinks, caption, listing_id):
        self.photoLinks = photoLinks
        self.caption = caption
        self.listing_id = listing_id #not really used since I didn't save these on file
    ##must have equals method to compare caption on ig to
    ##listing captions already on computer
    def __eq__(self, __o: object) -> bool:
        if self.caption != __o.caption:
            return False;
        return True;
#used to make the contents of message_c a string, not a html soup list        
def clean_message_c(message_c):
    len_mc = len(message_c)
    i=0
    new_message_c = []
    for message in message_c:
        if i%2==0:
            new_message_c.append(message)    
        i+=1
    return ''.join(new_message_c)
#used to tell scraper whether to overwrite a file, or if its already the same     
def is_str_in_file(strToFind, filename):
    if not os.path.exists(filename):
        f = open(filename,  "w")
        if strToFind == "":
            return True
        return False

    f = open(filename,  "r")
    if strToFind in f.read():
        return True
    return False
#downloads all the scraped listing info into Listings folder
def download_listings(listings):
    ## Trying to get 1st image to download
    instagram_album_cap = 10
    for j in range(len(listings)):
        ##save all images for each listing
        listing_dest = "Listings/Listing" +str(j)+"/"
        for i in range(len(listings[j].photoLinks)):
            if(i<instagram_album_cap):
                img_data = requests.get(listings[j].photoLinks[i]).content 
                destination = listing_dest+"photoLinks/"
                if not os.path.exists(destination):
                    os.makedirs(destination)
                destination = destination+"photo"+str(i)+".jpg"
                if not os.path.exists(destination):
                    with open(destination, 'wb') as handler: 
                        handler.write(img_data) 

        ##Trying to save message in files for each listing
        ## will overwrite the file if not same message
        text_file_dest = "Listings/Listing" +str(j)+"/message.txt"
        caption = listings[j].caption
        if not is_str_in_file(caption, text_file_dest): 
            text_file = open(text_file_dest, "w+")
            #put rent in caption
            n = text_file.write(caption)
            text_file.close()
##install chrome driver to navigate web
chromedriver_autoinstaller.install()
##give a display to launch chrome in virual env
# display = Display(visible=0, size=(800, 800))  
# display.start()
#Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument('--disable-dev-shm-usage')
##Run chrome
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome(ChromeDriverManager().install())
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
# driverPath = "~/Users/jackwalton/Code/chromedriver"
# driver = webdriver.Chrome(driverPath)
base_url = "https://welcomehomemanagementinc.appfolio.com"
url = "https://welcomehomemanagementinc.appfolio.com/listings?1659651846559&theme_color=%23676767&filters%5Border_by%5D=date_posted"
##launch chrom driver of listings page
driver.get(url)

##Scrolling all the way up
driver.maximize_window
driver.execute_script("window.scrollTo(0, 0);")

#Scroll down maximum amt
driver.execute_script("window.scrollTo(0,Math.max(document.documentElement.scrollHeight," + "document.body.scrollHeight,document.documentElement.clientHeight));")
#let stuff load on chrome
# time.sleep(2)
##get html of listings page
response = driver.page_source
html_soup = bs4.BeautifulSoup(response, "html5lib")
##grab all detail buttons associated links
details_containers = html_soup.find_all("a", {"class":"btn btn-secondary js-link-to-detail"})
##trying to keep track of main listings page
# parent = driver.current_window_handle
counter1 = 1
listings=[]

##go thru each 'details' links and grab all info in that page
for details in details_containers:
    counter2 = 1
    details_link = base_url + details["href"]
    # print(counter1,": ",details_link) ##print all details links for debug
    driver.get(details_link)
    response = driver.page_source
    html_soup = bs4.BeautifulSoup(response, "html5lib")
    
    ##containers to grab info on each listing's personalized page
    address_c = html_soup.find_all("h1", {"class":"fw-normal js-show-title"})
    info_c = html_soup.find_all("p", {"class":"header__summary js-show-summary"})
    images_c = html_soup.find_all("img")
    message_c = html_soup.find_all("p", {"class":"desk-hidden"})
    rent_c = html_soup.find_all("h2", {"class":"fw-normal d-inline-block"})
    messages = (clean_message_c(message_c[0].contents))

    limit = len(images_c)
    images_links = []
    # print("\n....images incoming....\n")
    for img in images_c:
        if limit > counter2:
            # print(img["src"])
            images_links.append(img["src"])
        counter2+=1

    # remove duplicated from list 
    images_links_final = [] 
    for img in images_links: 
        if img not in images_links_final: 
            images_links_final.append(img) 
        
    caption = info_c[0].contents[0].strip()+ "\n " +rent_c[0].contents[0].strip()+ "\n "+address_c[0].contents[0].strip()+ "\n " +messages
    listing = Listing(images_links_final, caption, counter1)
    listings.append(listing)
    counter1+=1

##MAIN POINT OF WEBSCRAPER IS TO DOWNLOAD "LISTINGS", DONE HERE
download_listings(listings)

# time.sleep(2)
driver.close()

##Original loop for grabbing images and printing urls
# for img in images:
#     image_src = img["href"]
#     print(number,": ",image_src)
#     number+=1
