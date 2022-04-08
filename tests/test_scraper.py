from scraper import IMDBScraper


def test_get_genres():
    s = IMDBScraper()

    movie_genres = s.get_genres(title_type="movies")
    tv_genres = s.get_genres(title_type="tv series")
    video_game_genres = s.get_genres(title_type="video games")

    # number of genres as of April 7, 2022
    assert len(movie_genres) == 24
    assert len(tv_genres) == 26
    assert len(video_game_genres) == 23
