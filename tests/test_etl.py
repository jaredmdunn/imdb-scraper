import os
import etl
import numpy
from pandas import DataFrame

from scraper import IMDBScraper


def test_store_tv_genres():
    old_last_modified: float = 0
    if os.path.isfile(etl.TOP_TV_GENRES_PATH):
        old_last_modified = os.path.getmtime(etl.TOP_TV_GENRES_PATH)
    etl.store_tv_genres()
    new_last_modified: float = os.path.getmtime(etl.TOP_TV_GENRES_PATH)
    # top tv genres parquet file exists
    assert os.path.exists(etl.TOP_TV_GENRES_PATH)
    # top tv genres parquet file was overwritten
    assert old_last_modified < new_last_modified


def test_store_top_50_series_by_genre():
    old_last_modified: float = 0
    if os.path.isfile(etl.TOP_50_SERIES_BY_GENRE_PATH):
        old_last_modified = os.path.getmtime(etl.TOP_50_SERIES_BY_GENRE_PATH)
    etl.store_top_50_series_by_genre()
    new_last_modified: float = os.path.getmtime(etl.TOP_50_SERIES_BY_GENRE_PATH)
    # top 50 series by genre file exists
    assert os.path.exists(etl.TOP_50_SERIES_BY_GENRE_PATH)
    # top 50 series by genre file was overwritten
    assert old_last_modified < new_last_modified


def test_read_tv_genres():
    tv_genres = etl.read_tv_genres()
    if os.path.isfile(etl.TOP_TV_GENRES_PATH):
        # expected number of genres
        assert len(tv_genres) == 26  # as of April 7, 2022
    else:
        # returns None if no file
        assert tv_genres == None


def test_read_top_50_series_by_genre_all():
    s: IMDBScraper = IMDBScraper()
    genres: list[str] = s.get_genres()
    top_50: DataFrame = etl.read_top_50_series_by_genre()
    if os.path.isfile(etl.TOP_50_SERIES_BY_GENRE_PATH):
        # matches tv genres on IMDB
        assert numpy.array_equal(top_50.columns, genres)

        for col_name, col_values in top_50.iteritems():
            # every column name is a current genre
            assert col_name in genres
            # every column has 50 entries
            assert len(col_values) == 50


def test_read_top_50_series_by_genre_good_genre():
    top_50_action: DataFrame = etl.read_top_50_series_by_genre(genres=["action"])
    if os.path.isfile(etl.TOP_50_SERIES_BY_GENRE_PATH):
        # only one column
        assert len(top_50_action.columns) == 1
        # column matches the specified name
        assert top_50_action.columns[0] == "action"
        # values is expected length of 50
        assert len(top_50_action.values == 50)
    else:
        # returns None if no file
        assert top_50_action == None


def test_read_top_50_series_by_genre_good_genre():
    top_50_action: DataFrame = etl.read_top_50_series_by_genre(genres=["foo"])
    if os.path.isfile(etl.TOP_50_SERIES_BY_GENRE_PATH):
        # zero columns
        assert len(top_50_action.columns) == 0
    else:
        # returns None if no file
        assert top_50_action == None
