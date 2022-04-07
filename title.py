from dataclasses import dataclass


@dataclass
class Title:
    """A class to hold titles (e.g., movie, tv series)"""

    genres: list[str]
    name: str
    rating: str
    runtime: int
    stars: float

    def __init__(
        self,
        name: str,
        genres: list[str] = None,
        rating: str = None,
        runtime: int = None,
        stars: str = None,
    ):
        self.name = name
        self.genres = genres
        self.runtime = runtime
        self.rating = rating
        self.stars = stars

    def __repr__(self) -> str:
        title_as_dict = {
            "genres": self.genres,
            "name": self.name,
            "rating": self.rating,
            "runtime": self.runtime,
            "stars": self.stars,
        }
        return f"{title_as_dict}"


@dataclass
class TitleRankingByTypeAndGenre:
    """A class to hold ranked titles by type and genre."""

    genres: list[str]
    title_types: list[str]
    titles: dict[int, Title]

    def __init__(
        self, genres: list[str], title_types: list[str], titles: dict[int, Title] = {}
    ):
        """Constructor for TitleRankingByTypeAndGenre.

        Args:
            genres (list[str]): A list of strings representing the genres associated with this ranking.
            title_types (list[str]): A list of strings representing the types associated with this ranking.
            titles (dict[int, Title]): A dictionary of rank (int) to Title. Defaults to an empty dictionary.
        """
        self.title_types = title_types
        self.genres = genres
        self.titles = titles

    def get_genres(self) -> list[str]:
        """Getter for genre list."""
        return self.genres.copy()

    def get_title_types(self) -> list[str]:
        """Getter for title types list."""
        return self.title_types.copy()

    def get_titles(self) -> dict[int, Title]:
        """Getter for titles dict."""
        return self.titles.copy()

    def get(self, rank: int) -> Title:
        """Get title by rank."""
        return self.titles.get(rank)

    def put(self, rank: int, title: Title):
        """Put a title into the ranking by rank."""
        self.titles[rank] = title

    def size(self) -> int:
        """Get the number of titles."""
        return len(self.get_titles())
