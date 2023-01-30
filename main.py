import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import string
from pandas import *
import imdb

import os
from dotenv import load_dotenv

# Import your netflix email and password from a .env file within the same directory
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


# Collection of the necessary urls. Profile url is dependent on your individual account
viewing_activity_url = "https://www.netflix.com/viewingactivity"
netflix_login_url = "https://www.netflix.com/login"
netflix_profile_url = "https://www.netflix.com/SwitchProfile?tkn=DB367CBI6BHJLMKLRCCNNTQTHU"

# Path to the netflix viewing history file (downloaded by the script)
viewing_history_path = "~/Downloads/NetflixViewingHistory.csv"


# Remove the previous viewing history file if it already exists
try:
    os.remove(os.path.expanduser(viewing_history_path))
except OSError:
    pass


class TV_Episode:
    instances = []
    punctuation = string.punctuation.replace("-", "")

    def __init__(self, show, season, episode):
        self.show = show
        self.season = season
        self.episode = episode
        TV_Episode.instances.append(self)

    def format(self):
        name = self.show.translate(str.maketrans('', '', self.punctuation))
        name = name.replace(" ", "-")
        name = name + "/" + self.season.replace(" ", "-")
        return name



class Movie:
    instances = []
    punctuation = string.punctuation.replace("-", "")
    
    def __init__(self, title, year = None):
        self.title = title
        self.year = year
        Movie.instances.append(self)

    # Formats the name of the movie to fit Tunefind url style. 
    # All punctuation except hyphens removed, spaces replaced by hyphens 
    # (Example: 'Avenger's: Endgame' ---->  'Avengers-Endgame-2019')
    def format(self) -> string:
        name = self.title.translate(str.maketrans('', '', self.punctuation))
        name = name.replace(" ", "-")
        name = name + "-" + str(self.year)
        return name



def separate_show_info(show_string, number_of_colons):
    if number_of_colons == 1:
        season = "Season 1"
        show, episode = show_string.split(": ")
        return show, season, episode





# Determines if a title is a TV show or movie
# Logic based on the conventions found in the netflix viewing history file
def classify(media):
    shows = []
    failure_count = 0

    for title in media:
        # Guaranteed to be a TV show
        if title.count(":") >= 2:
            shows.append(title)

        # One colon scenario (difficult to tell if it's a movie or one season show)
        # Decides that the title is a movie if the movie search result exactly matches the name
        else:
            results = ia.search_movie(title)
            if results and results[0]['title'] == title:
                try:
                    year = str(results[0]['year'])
                    Movie(title, year)
                except KeyError:
                    Movie(title)
                    print(title + "no year")
            
            # A title with no colon is definitely a movie, but the search didn't find it
            elif title.count(":") == 0:
                failure_count += 1

            # A one colon title that didn't appear in the movie search is assumed to be a show
            # Might update later to do a show search as well
            else:
                show, season, episode = separate_show_info(title, 1)
                TV_Episode(show, season, episode)

    return shows, failure_count





# Creates a new Chrome session
driver = webdriver.Chrome()
driver.implicitly_wait(30)

# Login procedure. Finds fields based on HTML tags
driver.get(netflix_login_url)
driver.find_element(By.XPATH, """//*[@id="id_userLoginId"]""").send_keys(EMAIL_ADDRESS)
driver.find_element(By.XPATH, """//*[@id="id_password"]""").send_keys(PASSWORD)
driver.find_element(By.XPATH, '//button[text()="Sign In"]').click()
driver.get(netflix_profile_url)
driver.get(viewing_activity_url)
driver.find_element(By.XPATH, "//*[text()='Download all']").click()
time.sleep(5)


# Reads in the downloaded file and movies all the media titles to a list
viewing_history = read_csv(os.path.expanduser(viewing_history_path))
titles = viewing_history["Title"].to_list()


# Separates the movies and TV shows to format correctly (some failures in classification currently)
ia = imdb.IMDb()
shows, failure_count = classify(titles)
print(failure_count)

for episode in TV_Episode.instances:
    print(episode.format())     





""" driver.get("https://www.tunefind.com/show/the-magicians/season-1/27673")

songs = []
artists = []

soup = BeautifulSoup(driver.page_source, "html.parser")

elems = driver.find_elements(By.XPATH, "//a[@href]")

for elem in elems:
    if "song" in elem.get_attribute("href"):
        songs.append(elem.get_attribute("href")) """




# Removes the netflix viewing history file
os.remove(os.path.expanduser(viewing_history_path))