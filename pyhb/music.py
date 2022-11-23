import typing as _t

import bs4 as _bs4
import click as _click
import pytube as _pytube
import requests as _requests

import pyhb.cli.colors
import pyhb.cli.io
from pyhb.common import INVALID_SONG_DISPLAY_MSG


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


def get_song_from_list(songs: _t.Dict[str, str]) -> str:
    """Retrieves a song from a list of options"""
    pyhb.cli.io.list_options(songs, pyhb.cli.colors.OutputColorScheme.RANDOM)
    option = pyhb.cli.io.get_option("Choose a song: ", list(songs.values()))
    return option


def get_song_url(song: str, songs: _t.Dict[str, str]) -> str:
    """Returns a song from the songs dictionary if it is valid."""
    if song in songs:
        return songs[song]
    else:
        _click.echo(INVALID_SONG_DISPLAY_MSG.format(song=song))
        exit()
