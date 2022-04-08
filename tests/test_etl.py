import os
import etl


def test_store_genres():
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
