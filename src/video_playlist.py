"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, playlist_name: str):
        self._playlist_name = playlist_name
        self._playlist_videos = []

    @property
    def playlist_name(self) -> str:
        """Returns the name of a playlist."""
        return self._playlist_name

    @property
    def playlist_videos(self) -> list[str]:
        """Returns the list of video ids which are in playlist."""
        return self._playlist_videos
