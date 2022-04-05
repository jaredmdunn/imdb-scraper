def main():
    # IMDB link: https://www.imdb.com/feature/genre?ref_=fn_asr_ge

    # Plan of attach:
    # 1. Grab popular tv series genres and their links from IMBD link
    #    (store as dict -> convert to pandas dataframe -> convert to parquet file)
    # USE [dataclass](https://docs.python.org/3/library/dataclasses.html)?
    # 2. Loop through genres and collect top 50 tv shows from each:
    #    store show title, rank, rating, year, etc. array of TVSeries
    # 3. Convert array to dataframe to parquet file

    pass


if __name__ == "__main__":
    main()
