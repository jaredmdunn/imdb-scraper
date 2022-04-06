from bs4 import BeautifulSoup, PageElement, Tag, ResultSet
import requests
from typing import Callable

from tv_series import TVGenre, TVSeries


class TVSeriesScraper:
    imdb_genre_link: str

    def __init__(self, imdb_genre_link: str):
        """Constructor for TVSeriesScraper

        Args:
            imdb_genre_link (str): link to the page with top TV genres
        """
        self.imdb_genre_link = imdb_genre_link

    def load_genres(self) -> list[TVGenre]:
        page = requests.get(self.imdb_genre_link)
        soup = BeautifulSoup(page.content, "html.parser")

        h3s: ResultSet = soup.find_all("h3")

        def is_tv_genre_link_div(tag: Tag):

            tv_genre_header = None
            for h3 in h3s:
                if "TV Series by Genre" in h3.string:
                    tv_genre_header = h3
                    break

            return (
                "class" in tag.attrs
                and "ab_links" in tag.attrs.get("class")
                and tag.find(lambda elem: elem is tv_genre_header)
            )

        tv_genre_div: Tag = soup.find_all(is_tv_genre_link_div)[0]

        tv_genre_links = tv_genre_div.find_all("a")

        tv_genres: list[TVGenre] = []
        for elem in tv_genre_links:
            name = elem.string.strip()
            link = elem.attrs["href"]

            genre = TVGenre(name=name, link=link)

            tv_genres.append(genre)

        return tv_genres
