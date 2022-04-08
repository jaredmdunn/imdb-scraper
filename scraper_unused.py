import requests
from bs4 import BeautifulSoup, ResultSet, Tag

from title import Title, TitleRankingByTypeAndGenre


# I tried to use my own custom data types, but had issues
# when I needed to save theminto the parquet files so I
# abandoned this method.


def get_top_50(
    self,
    genres: list[str] = ["action"],
    title_types: list[str] = ["tv series", "mini series"],
) -> TitleRankingByTypeAndGenre:
    """Gets the top 50 for any given title types and genres

    Args:
        genres (list[str], optional): A list of genres. Defaults to ["action"].
        title_types (list[str], optional): A list of title types. Defaults to ["tv series", "mini series"].

    Returns:
        TitleRankingByTypeAndGenre: A ranking of titles by the specified genres and types.
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

    top_50: TitleRankingByTypeAndGenre = TitleRankingByTypeAndGenre(
        title_types=title_types, genres=genres, titles={}
    )
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
            logging.info(f"Missing genre for {name}:\n{elem}")
        if not rating:
            logging.info(f"Missing rating for {name}:\n{elem}")
        if not runtime:
            logging.info(f"Missing runtime for {name}:\n{elem}")
        if not stars:
            logging.info(f"Missing stars for {name}:\n{elem}")

        title_obj = Title(
            genres=genres,
            name=name,
            rating=rating,
            runtime=runtime,
            stars=stars,
        )

        top_50.put(rank, title_obj)

    return top_50
