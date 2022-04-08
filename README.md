# imdb-scraper
A Python web scraper to get info on movies and series from IMDB.

## To Run:
  1. Run `pip install -r requirements.txt` to set up your virtual environment.
  2. At the **imdb-scraper** directory run `python main.py`.

## Scraper (scraper.py)
**scraper.py** includes a `IMDBScraper` class with two methods: `get_genres` and `get_top_50_as_dict`.

`get_genre` can be used to get top genres listed on IMDB's [featured genres page](https://www.imdb.com/feature/genre/)

`get_top_50_as_dict` utilizes IMDB's [title search page](https://www.imdb.com/search/title/) to get the top 50 listed for any set of genres and title types (in the query string).

## ETL (etl.py)
**etl.py** includes four methods that make getting info on tv series very straight forward.

`store_tv_genres` stores the top tv genres listed into a parquet file in the storage folder.

`read_tv_genres` reads the genres from the tv genres storage parquet file.

`store_top_50_series_by_genre` stores the top 50 tv titles for each featured tv genre into a parquet file.

`read_top_50_series_by_genre` reads the genres from the top 50 storage parquet file.

## Tests
I wrote basic unit tests for the IMDBScraper and the ETL functions. It could definitely be tested more thoroughly.

To test, run `pytest`.

If you get a ModuleNotFoundError, you may need to update your virtual environment `PYTHONPATH`:

```export PYTHONPATH="{$PYTHONPATH}:/path/to/project/root/"```

## Unused (title.py and scraper_unused.py)
Initially, I tried to use my own custom data types, but had issues when I needed to save them into the parquet files so I abandoned this method.