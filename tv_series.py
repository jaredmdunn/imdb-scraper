from dataclasses import dataclass


@dataclass()
class TVGenre:
    """
    A class to hold tv genres and their corresponding IMDB link
    """

    name: str
    link: str

    def __init__(self, name, link):
        self.name = name
        self.link = link


@dataclass()
class TVSeries:
    """
    A class to hold TV series
    """

    title: str
