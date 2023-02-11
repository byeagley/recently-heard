import string

class TV_Episode:
    instances = []
    punctuation = string.punctuation.replace("-", "")

    def __init__(self, show, season, episode):
        self.show = show
        self.season = season
        self.episode = episode
        TV_Episode.instances.append(self)


    # Formats the show info to fit Tunefind url style
    # All punctuation except hyphens removed, spaces replaced by hyphens
    # Show name followed by season (Example: "Community: Season 4" ----> "Community/Season-4")
    def format(self):
        name = self.show.translate(str.maketrans('', '', self.punctuation))
        name = name.replace(" ", "-")
        name = name + "/" + self.season.replace(" ", "-")
        return name