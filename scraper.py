from bs4 import BeautifulSoup, Tag, ResultSet
import requests


class IMDBScraper:
    """A class to scrape IMDB for movie and tv information."""

    BASE_URL: str = "https://www.imdb.com"

    genre_path: str
    search_path: str

    def __init__(
        self, genre_path: str = "/feature/genre", search_path: str = "/search/title"
    ):
        """Constructor for an IMDBScraper.

        Args:
            genre_path (str, optional): Specifies the path to access featured genres. Defaults to "/feature/genre".
            search_path (str, optional): Specifies the path to search over different titles. Defaults to "/search/title".
        """
        self.genre_path = genre_path
        self.search_path = search_path

    def get_genres(self, title_type: str = "tv series") -> list[str]:
        """Gets a list of genres for a specific type.

        Args:
            title_type (str, optional): A string that corresponds to title type. Defaults to "tv series".

        Returns:
            list[str]: A list of lowercase strings corresponding to the genres for a specified type.
        """

        page = requests.get(self.BASE_URL + self.genre_path)
        soup: BeautifulSoup = BeautifulSoup(page.content, "html.parser")

        title_type_headers: ResultSet[Tag] = soup.find_all("h3")

        def is_links_div_for_title_type(tag: Tag):
            type_header = None
            for header in title_type_headers:
                if f"{title_type} by genre" in header.string.lower():
                    type_header = header
                    break

            return (
                "class" in tag.attrs
                and "ab_links" in tag.attrs.get("class")
                and tag.find(lambda elem: elem is type_header)
            )

        title_type_div = soup.find(is_links_div_for_title_type)

        genre_links = title_type_div.find_all("a")

        genres = [link.string.strip().lower() for link in genre_links]

        return genres

    def get_top_50(
        self,
        genres: list[str] = ["action"],
        title_types: list[str] = ["tv series", "mini series"],
    ) -> list[dict]:
        """Gets the top 50 for any given title types and genres

        Args:
            genres (list[str], optional): A list of genres. Defaults to ["action"].
            title_types (list[str], optional): A list of title types. Defaults to ["tv series", "mini series"].

        Returns:
            list[dict]: A list of title objects that hold the name and rank of different titles.
        """
        genres_string: str = ""

        for genre in genres:
            genres_string += genre.replace(" ", "-") + ","

        title_types_string: str = ""

        for title_type in title_types:
            title_types_string += title_type.replace(" ", "_") + ","

        url: str = f"{self.BASE_URL}{self.search_path}?genres={genres_string}&title_type={title_types_string}"

        page = requests.get(url)
        soup: BeautifulSoup = BeautifulSoup(page.content, "html.parser")

        titles: ResultSet[Tag] = soup.find_all("h3", {"class", "lister-item-header"})

        top_50: list[dict] = []
        for title in titles:
            name: str = title.find("a").string
            rank: int = int(
                float(title.find(True, {"class", "lister-item-index"}).string)
            )

            title_obj: dict = {"name": name, "rank": rank}
            top_50.append(title_obj)

        return top_50
