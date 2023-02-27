class Song:
    instances = []

    def __init__(self, track, artist):
        self.track = track
        self.artist = artist
        Song.instances.append(self)
        