class Song:
    instances = []

    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        Song.instances.append(self)
        