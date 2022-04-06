from bs4 import BeautifulSoup, Tag
import requests
from typing import Callable

from tv_series import TVGenre, TVSeries


class IMDBScraper:
    BASE_URL: str = "https://www.imdb.com"

    genre_path: str
    search_path: str

    def __init__(
        self, genre_path: str = "/feature/genre", search_path: str = "/search/title/"
    ):
        self.genre_path = genre_path
        self.search_path = search_path

    def get_genres(self, media_type: str = "tv series") -> list[str]:
        """Gets a list of genres for a specific type.

        Args:
            type (str, optional): A string that corresponds to media type. Defaults to "tv series".

        Returns:
            list[str]: A list of lowercase strings corresponding to the genres for a specified type.
        """

        page = requests.get(self.BASE_URL + self.genre_path)
        soup = BeautifulSoup(page.content, "html.parser")

        media_type_headers = soup.find_all("h3")

        def is_links_div_for_media_type(tag: Tag):
            type_header = None
            for header in media_type_headers:
                if f"{media_type} by genre" in header.string.lower():
                    type_header = header
                    break

            return (
                "class" in tag.attrs
                and "ab_links" in tag.attrs.get("class")
                and tag.find(lambda elem: elem is type_header)
            )

        media_type_div = soup.find(is_links_div_for_media_type)

        genre_links = media_type_div.find_all("a")

        genres = [link.string.strip().lower() for link in genre_links]

        return genres
