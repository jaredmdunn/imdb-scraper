import pandas
from pandas import DataFrame
import os

from scraper import IMDBScraper


TOP_TV_GENRES_PATH = "storage/top_tv_genres.parquet"
TOP_50_SERIES_BY_GENRE_PATH = "storage/top_50_series_by_genre.parquet"


def store_tv_genres():
    s = IMDBScraper()
    tv_genres: list[str] = s.get_genres()
    DataFrame(data=tv_genres, columns=["genre"]).to_parquet(path=TOP_TV_GENRES_PATH)


def read_tv_genres() -> DataFrame:
    if not os.path.isfile(TOP_TV_GENRES_PATH):
        return None
    return pandas.read_parquet(path=TOP_TV_GENRES_PATH)


def store_top_50_series_by_genre():
    top_50_series_by_genre: dict = {}
    s = IMDBScraper()
    tv_genres: list[str] = s.get_genres()

    for genre in tv_genres:
        top_50 = s.get_top_50_as_dict(genres=[genre])
        top_50_series_by_genre[genre] = top_50

    data: DataFrame = DataFrame(data=top_50_series_by_genre)
    data.to_parquet(path=TOP_50_SERIES_BY_GENRE_PATH)


def read_top_50_series_by_genre(genres: list[str] = None) -> DataFrame:
    if not os.path.isfile(TOP_50_SERIES_BY_GENRE_PATH):
        return None

    if genres:
        try:
            return pandas.read_parquet(path=TOP_50_SERIES_BY_GENRE_PATH, columns=genres)
        except:
            return DataFrame()
    else:
        return pandas.read_parquet(path=TOP_50_SERIES_BY_GENRE_PATH)
