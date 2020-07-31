import os

DATA_PATH = 'places/data/'


class Place:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.photos = []


places_list = []

for dirname in os.listdir(DATA_PATH):
    dirpath = os.path.join(DATA_PATH, dirname)
    if os.path.isdir(dirpath):
        place = Place(dirname)
        for filename in os.listdir(dirpath):
            if filename.endswith(".txt"):
                with open(filename, 'r') as file:
                    place.description = "\n".join(file)
            if filename.endswith(".jpg"):
                place.photos.append(filename)
        places_list.append(place)

print(places_list)
