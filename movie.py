import string

class Movie:
    instances = []
    punctuation = string.punctuation.replace("-", "")
    
    def __init__(self, title, year = None):
        self.title = title
        self.year = year
        Movie.instances.append(self)

    # Formats the name of the movie to fit Tunefind url style
    # All punctuation except hyphens removed, spaces replaced by hyphens 
    # (Example: "Avenger's: Endgame" ---->  "Avengers-Endgame-2019")
    def format(self) -> string:
        name = self.title.translate(str.maketrans('', '', self.punctuation))
        name = name.replace(" ", "-")
        name = name + "-" + str(self.year)
        return name
