import typing as _t

import bs4 as _bs4
import pytube as _pytube
import requests as _requests


class InvalidYTUrl(Exception):
    """A class for invalid YouTube URLs"""


def get_title_from_url(url: str) -> str:
    """Gets a title from a given URL."""
    resp = _requests.get(url)
    soup = _bs4.BeautifulSoup(resp.text, "html.parser")

    if soup.title is None:
        raise InvalidYTUrl("Invalid YT url.")

    return soup.title.text


def scrape_songs_from_playlist(playlist_url: str) -> _t.Dict[str, str]:
    """Returns a list of video titles and their URLs
    from a given playlist."""

    playlist = _pytube.Playlist(playlist_url)

    songs = {}
    for url in playlist.video_urls:
        title = get_title_from_url(url)
        songs[title] = url

    return songs
