from scraper import IMDBScraper


def test_get_genres():
    s = IMDBScraper()

    default_genres = s.get_genres()  # same as tv series
    movie_genres = s.get_genres(title_type="movies")
    tv_genres = s.get_genres(title_type="tv series")
    video_game_genres = s.get_genres(title_type="video games")

    # number of genres as of April 7, 2022
    assert len(default_genres) == 26
    assert len(movie_genres) == 24
    assert len(tv_genres) == 26
    assert len(video_game_genres) == 23


def test_get_top_50_as_dict():
    s = IMDBScraper()

    default_top_50 = (
        s.get_top_50_as_dict()
    )  # same as ["action"], ["tv series", "mini series"]

    action_movies_top_50 = s.get_top_50_as_dict(["action"], ["movies"])

    assert len(default_top_50.items()) == 50
    assert len(action_movies_top_50.items()) == 50
