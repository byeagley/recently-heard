class TV_Episode:
    instances = []

    def __init__(self, show, season, episode):
        self.show = show
        self.season = season
        self.episode = episode
        TV_Episode.instances.append(self)
    





