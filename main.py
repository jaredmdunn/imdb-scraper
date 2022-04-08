import etl


def main():
    """
    Store top tv genres and top 50 series in parquet files.
    Then read and print them out.
    """
    etl.store_tv_genres()
    etl.store_top_50_series_by_genre()

    genres = etl.read_tv_genres()
    top_50_series_by_genre = etl.read_top_50_series_by_genre()

    top_50_action_series = etl.read_top_50_series_by_genre(genres=["action"])

    print(genres)
    print(top_50_series_by_genre)
    print(top_50_action_series)


if __name__ == "__main__":
    main()
