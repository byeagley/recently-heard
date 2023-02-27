import string
from selenium.webdriver.common.by import By
from song import Song
import time


class TV_Episode:
    instances = []
    punctuation = string.punctuation.replace("-", "")
    general_url = "https://www.tunefind.com/show/"

    def __init__(self, show, season, episode, url = None):
        self.show = show
        self.season = season
        self.episode = episode
        self.url = url
        TV_Episode.instances.append(self)



    def get_url(self, webdriver):
        name = self.show.translate(str.maketrans('', '', self.punctuation))
        name = name.replace(" ", "-")
        name = name + "/" + self.season.replace(" ", "-")
        season_url = self.general_url + name + "/"
        season_url = season_url.lower()

        webdriver.get(season_url)
        time.sleep(6)
        # Tunefind Page not Found standard
        if "Page not found" in webdriver.page_source:
            return None

        h3_tags = webdriver.find_elements(By.CLASS_NAME, "EpisodeListItem_title__PkSzj")
        #a_tags = h3_tags.find_elements(By.TAG_NAME, "a")

        for tag in h3_tags:
            a_tag = tag.find_element(By.TAG_NAME, "a")
            if self.episode in a_tag.text:
                self.url = a_tag.get_attribute("href")

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

    





