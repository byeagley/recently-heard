import string
from selenium.webdriver.common.by import By
from song import Song
import time

class Movie:
    instances = []
    punctuation = string.punctuation.replace("-", "")
    general_url = "https://www.tunefind.com/movie/"
    
    def __init__(self, title, year = None, url = None, soundtrack = None):
        self.title = title
        self.year = year
        self.soundtrack = soundtrack
        Movie.instances.append(self)
    

    def get_url(self, webdriver):
        name = self.title.translate(str.maketrans('', '', self.punctuation))
        name = name.replace(" ", "-")
        name = name + "-" + str(self.year)
        self.url = self.general_url + name

        return self.url
    

    def get_soundtrack(self, webdriver):
        self.soundtrack = []
        webdriver.get(self.url)
        time.sleep(6)
        # Tunefind Page not Found standard
        if "Page not found" in webdriver.page_source:
            return None

        titles = webdriver.find_elements(By.CLASS_NAME, "SongTitle_link__qlRUV")
        artists = webdriver.find_elements(By.CLASS_NAME, "SongEventRow_subtitle__Zal_J")

        for i in range(len(titles)):
            self.soundtrack.append(Song(titles[i].text, artists[i].text))

        return self.soundtrack
