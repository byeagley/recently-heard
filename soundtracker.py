from selenium import webdriver
from selenium.webdriver.common.by import By

from song import Song
from movie import Movie, Tunefind_Movie

def main():
    URL = "https://www.tunefind.com/movie/the-martian-2015"


    # Creates a new Chrome session
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)

    driver.get(URL)
    songs = driver.find_elements(By.CLASS_NAME, "SongTitle_link__qlRUV")
    artists = driver.find_elements(By.CLASS_NAME, "SongEventRow_subtitle__Zal_J")

    for i in range(len(songs)):
        Song(songs[i].text, artists[i].text)


    Tunefind_Movie("test", "test", "test")
    Movie("test", "test", "test")

    print(len(Tunefind_Movie.instances))





if __name__ == "__main__":
    main()