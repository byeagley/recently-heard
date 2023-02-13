import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from pandas import *
import imdb
import string
import os
from dotenv import load_dotenv


from movie import Movie
from episode import TV_Episode


# Collection of the necessary urls. Profile url is dependent on your individual account
viewing_activity_url = "https://www.netflix.com/viewingactivity"
netflix_login_url = "https://www.netflix.com/login"
netflix_profile_url = "https://www.netflix.com/SwitchProfile?tkn=DB367CBI6BHJLMKLRCCNNTQTHU"
tunefind_url = "https://tunefind.com/"

# Path to the netflix viewing history file (downloaded by the script)
viewing_history_path = "~/Downloads/NetflixViewingHistory.csv"


# List of words used for "season" (so far)
season_words = ["Season", "Part", "Chapter", "Book", "Volume", "Limited Series"]




# Changes the season portion to always be "Season (some number)"
def rewrite(season):
    season_number = 1
    for c in season:
            if c.isdigit():
                season_number = c
    season = "Season " + str(season_number)
    return season





def separate_episode_info(full_show_info, number_of_colons):

    # Must only contain the show and episode name, season implied to be 1
    if number_of_colons == 1:
        season = "Season 1"
        show, episode = full_show_info.split(": ")
    
    # Most likely formatted as ---- Show: Season: Episode
    elif number_of_colons == 2:
        show, season, episode = full_show_info.split(": ")

        # Catches cases like ---- Show Header: Show Subheader: Episode ---- by assuming season 1
        if not any(word in season for word in season_words):
            show = show + season
            season = "Season 1"
        elif "Season" not in season:
            season = rewrite(season)

    # Complicated case
    # Tries to find the season info, then assumes everything before it is the show and everything after is the episode
    elif number_of_colons >= 3:
        components = full_show_info.split(": ")
        # Loop assumes the first and last item definitely aren't the season info
        for i in range(1, len(components) - 1):
            # Probably found the season info
            if any(word in components[i] for word in season_words):
                season = rewrite(components[i])
                show = components[:i]
                show = ': '.join(show)
                episode = components[i+1:]
                episode = ': '.join(episode)
                return show, season, episode

        print(full_show_info)
        return "ERROR", "ERROR", "ERROR"

    
    return show, season, episode

 





# Determines if a title is a TV show or movie
# Logic based on the conventions found in the netflix viewing history file
def classify(media):

    classified_media = []

    for title in media:
        ia = imdb.IMDb()

        colon_count = title.count(":")

        # Guaranteed to be a TV show
        if colon_count >= 2:
            show, season, episode = separate_episode_info(title, colon_count)
            classified_media.append(TV_Episode(show, season, episode))

        # One colon scenario (difficult to tell if it's a movie or one season show)
        # Decides that the title is a movie if the movie search result exactly matches the name
        else:
            results = ia.search_movie(title)
            if results and results[0]['title'] == title:
                try:
                    year = str(results[0]['year'])
                    classified_media.append(Movie(title, year))
                except KeyError:
                    print(title)
            
            # A title with no colon is definitely a movie, but the search didn't find it
            elif colon_count == 0:
                print(title)

            # A one colon title that didn't appear in the movie search is assumed to be a show
            # Might update later to do a show search as well
            else:
                show, season, episode = separate_episode_info(title, 1)
                classified_media.append(TV_Episode(show, season, episode))


    return classified_media



def get_movie_url(movie):
    punctuation = string.punctuation.replace("-", "")
    url = "tunefind.com/movie/"

    name = movie.title.translate(str.maketrans('', '', punctuation))
    name = name.replace(" ", "-")
    name = name + "-" + str(movie.year)
    tunefind_url = url + name
    return tunefind_url


def get_season_url(episode):
    punctuation = string.punctuation.replace("-", "")
    url = "tunefind.com/show/"

    name = episode.show.translate(str.maketrans('', '', punctuation))
    name = name.replace(" ", "-")
    name = name + "/" + episode.season.replace(" ", "-")
    tunefind_url = url + name + "/"
    return tunefind_url









def main():
    # Remove the previous viewing history file if it already exists
    try:
        os.remove(os.path.expanduser(viewing_history_path))
    except OSError:
        pass



    # Import your netflix email and password from a .env file within the same directory
    load_dotenv()
    EMAIL_ADDRESS = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")


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
    # Wait for the file to download
    time.sleep(10)


    # Reads in the downloaded file and moves all the media titles to a list
    viewing_history = read_csv(os.path.expanduser(viewing_history_path))
    titles = viewing_history["Title"].to_list()


    # Separates the movies and TV shows to format correctly (some failures in classification currently)
    list = classify(titles)

    for item in list:
        if isinstance(item, Movie):
            print(get_movie_url(item))


    # Removes the netflix viewing history file
    os.remove(os.path.expanduser(viewing_history_path))

    
    return



if __name__ == "__main__":
    main()



