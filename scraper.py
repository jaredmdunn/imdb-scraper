from bs4 import BeautifulSoup, Tag, ResultSet
import logging
import requests

# set up info logging
logging.basicConfig(
    filename="info.log", encoding="utf-8", level=logging.INFO, filemode="w"
)


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

        def is_links_div_for_title_type(tag: Tag) -> bool:
            """Helper function to check if the links div is the proper one.

            Args:
                tag (Tag): the tag to check

            Returns:
                bool: whether the tag is the links div for the specified title type
            """
            type_header: Tag = None
            for header in title_type_headers:
                if f"{title_type} by genre" in header.string.lower():
                    type_header = header
                    break

            return (
                "class" in tag.attrs
                and "ab_links" in tag.attrs.get("class")
                and tag.find(lambda elem: elem is type_header)
            )

        title_type_div: Tag = soup.find(is_links_div_for_title_type)

        genre_links: ResultSet[Tag] = title_type_div.find_all("a")

        genres = [link.string.strip().lower() for link in genre_links]

        return genres

    def get_top_50_as_dict(
        self,
        genres: list[str] = ["action"],
        title_types: list[str] = ["tv series", "mini series"],
    ) -> dict:
        """Gets the top 50 for any given title types and genres

        Args:
            genres (list[str], optional): A list of genres. Defaults to ["action"].
            title_types (list[str], optional): A list of title types. Defaults to ["tv series", "mini series"].

        Returns:
            dict: A ranking of titles for the specified genres and title types.
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

        title_elements: ResultSet[Tag] = soup.find_all(
            "div", {"class", "lister-item-content"}
        )

        top_50: dict = {}
        for elem in title_elements:
            # if name link exists, get name
            name_header: Tag = elem.find("h3", {"class": "lister-item-header"})
            name_link: Tag = name_header.find("a") if name_header else None
            name: str = (name_link.string) if name_link else None

            # if there isn't a name throw exception
            if not name:
                raise Exception("Title is missing name.")

            # if elem has rank, get rank
            rank_span: Tag = elem.find("span", {"class", "lister-item-index"})
            rank: int = int(float(rank_span.string)) if rank_span else None

            # if there isn't a ranking throw exception
            if not rank:
                raise Exception(f"Title {name} is missing rank.")

            # if elem has span with genres, get genres
            genre_span: Tag = elem.find("span", {"class": "genre"})
            genres: list[str] = (
                [genre.lower().strip() for genre in genre_span.string.split(",")]
                if genre_span
                else None
            )

            # if elem has rating span, get rating
            rating_span: Tag = elem.find("span", {"class", "certificate"})
            rating: str = rating_span.string.strip() if rating_span else None

            # if elem has runtime span, get runtime
            runtime_span: Tag = elem.find("span", {"class", "runtime"})
            runtime: int = (
                int(runtime_span.string.split()[0].replace(",", ""))
                if runtime_span
                else None
            )

            # if elem has ratings-bar div and strong, get star rating
            ratings_bar: Tag = elem.find("div", {"class": "ratings-bar"})
            stars_strong: Tag = ratings_bar.find("strong") if ratings_bar else None
            stars: float = float(stars_strong.string.strip()) if stars_strong else None

            # logging
            if not genre:
                logging.info(f"Missing genre for {name}.")
            if not rating:
                logging.info(f"Missing rating for {name}.")
            if not runtime:
                logging.info(f"Missing runtime for {name}.")
            if not stars:
                logging.info(f"Missing stars for {name}.")

            title_dict = {
                "genres": genres,
                "name": name,
                "rating": rating,
                "runtime": runtime,
                "stars": stars,
            }

            top_50[rank] = title_dict

        return top_50
