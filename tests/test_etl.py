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
    assert os.path.exists(etl.TOP_TV_GENRES_PATH)
    assert old_last_modified < new_last_modified


def test_store_top_50_series_by_genre():
    old_last_modified: float = 0
    if os.path.isfile(etl.TOP_50_SERIES_BY_GENRE_PATH):
        old_last_modified = os.path.getmtime(etl.TOP_50_SERIES_BY_GENRE_PATH)
    etl.store_top_50_series_by_genre()
    new_last_modified: float = os.path.getmtime(etl.TOP_50_SERIES_BY_GENRE_PATH)
    assert os.path.exists(etl.TOP_50_SERIES_BY_GENRE_PATH)
    assert old_last_modified < new_last_modified


def test_read_tv_genres():
    tv_genres = etl.read_tv_genres()
    if os.path.isfile(etl.TOP_TV_GENRES_PATH):
        assert len(tv_genres) == 26  # as of April 7, 2022
    else:
        assert tv_genres == None


def test_read_top_50_series_by_genre_all():
    s: IMDBScraper = IMDBScraper()
    genres: list[str] = s.get_genres()
    top_50: DataFrame = etl.read_top_50_series_by_genre()
    if os.path.isfile(etl.TOP_50_SERIES_BY_GENRE_PATH):
        assert numpy.array_equal(top_50.columns, genres)

        for col in top_50.iteritems():
            assert len(col[1]) == 50
