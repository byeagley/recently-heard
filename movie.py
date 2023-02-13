class Movie:
    instances = []
    
    def __init__(self, title, year = None, soundtrack = None):
        self.title = title
        self.year = year
        self.soundtrack = soundtrack
        Movie.instances.append(self)
    

