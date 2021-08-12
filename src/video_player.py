"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import operator
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlists = []
        self._playing_video = None
        self._playing_video_state = 0  # 0-not paused, 1-paused

    def number_of_videos(self):
        num_videos = len([video for video in self._video_library.get_all_videos() if video.flag is None])
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = sorted(self._video_library.get_all_videos(), key=operator.attrgetter("title"))
        print("Here's a list of all available videos:")
        for video in all_videos:
            if video.flag is None:
                print(video)
            else:
                print(f"{video} - FLAGGED (reason: {video.flag})")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot play video: Video does not exist")
        else:
            if self._playing_video is not None:
                video_to_stop = self._video_library.get_video(self._playing_video)
                print(f"Stopping video: {video_to_stop.title}")
                self._playing_video = None

            if video.flag is None:
                self._playing_video = video.video_id
                self._playing_video_state = 0
                print(f"Playing video: {video.title}")
            else:
                print(f"Cannot play video: Video is currently flagged (reason: {video.flag})")

    def stop_video(self):
        """Stops the current video."""
        if self._playing_video is not None:
            video_to_stop = self._video_library.get_video(self._playing_video)
            print(f"Stopping video: {video_to_stop.title}")
            self._playing_video = None
            self._playing_video_state = 0
        else:
            print(f"Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        video = random.choice(self._video_library.get_all_videos())
        if video is not None and video.flag is None:
            self.play_video(video.video_id)
        else:
            print("No videos available")

    def pause_video(self):
        """Pauses the current video."""
        video = self._video_library.get_video(self._playing_video)
        video_state = self._playing_video_state

        if video and video_state == 0:
            self._playing_video_state = 1
            print(f"Pausing video: {video.title}")
        elif video and video_state == 1:
            print(f"Video already paused: {video.title}")
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        video = self._video_library.get_video(self._playing_video)
        video_state = self._playing_video_state

        if video and video_state == 1:
            self._playing_video_state = 0
            print(f"Continuing video: {video.title}")
        elif video and video_state == 0:
            print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        video = self._video_library.get_video(self._playing_video)
        video_state = self._playing_video_state

        if video is not None:
            if video_state == 1:
                print(f"Currently playing: {video} - PAUSED")
            else:
                print(f"Currently playing: {video}")
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in (playlist.playlist_name.upper() for playlist in self._playlists):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlists.append(Playlist(playlist_name))
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video = self._video_library.get_video(video_id)
        if playlist_name.upper() not in (playlist.playlist_name.upper() for playlist in self._playlists):
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        else:
            if video:
                for playlist in self._playlists:
                    if playlist_name.upper() == playlist.playlist_name.upper():
                        if video_id in playlist.playlist_videos:
                            print(f"Cannot add video to {playlist_name}: Video already added")
                        else:
                            if video.flag is None:
                                playlist.playlist_videos.append(video_id)
                                print(f"Added video to {playlist_name}: {video.title}")
                            else:
                                print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video.flag})")
            else:
                print(f"Cannot add video to {playlist_name}: Video does not exist")

    def show_all_playlists(self):
        """Display all playlists."""
        playlists = sorted(self._playlists, key=operator.attrgetter("playlist_name"))
        if playlists:
            print("Showing all playlists:")
            for playlist in playlists:
                print(playlist.playlist_name)
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in (playlist.playlist_name.upper() for playlist in self._playlists):
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
        else:
            for playlist in self._playlists:
                if playlist_name.upper() == playlist.playlist_name.upper():
                    print(f"Showing playlist: {playlist_name}")
                    if playlist.playlist_videos:
                        for playlist_video in playlist.playlist_videos:
                            video = self._video_library.get_video(playlist_video)
                            if video.flag is None:
                                print(video)
                            else:
                                print(f"{video} - FLAGGED (reason: {video.flag})")
                    else:
                        print("No videos here yet")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        video = self._video_library.get_video(video_id)
        if playlist_name.upper() not in (playlist.playlist_name.upper() for playlist in self._playlists):
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            if video:
                for playlist in self._playlists:
                    if playlist_name.upper() == playlist.playlist_name.upper():
                        if video_id in playlist.playlist_videos:
                            playlist.playlist_videos.remove(video_id)
                            print(f"Removed video from {playlist_name}: {video.title}")
                        else:
                            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            else:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in (playlist.playlist_name.upper() for playlist in self._playlists):
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            for playlist in self._playlists:
                if playlist_name.upper() == playlist.playlist_name.upper():
                    playlist.playlist_videos.clear()
                    print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in (playlist.playlist_name.upper() for playlist in self._playlists):
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            for playlist in self._playlists:
                if playlist_name.upper() == playlist.playlist_name.upper():
                    self._playlists.remove(playlist)
                    print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = sorted(self._video_library.get_all_videos(), key=operator.attrgetter("title"))
        found_videos = []
        for video in all_videos:
            if search_term.upper() in video.title.upper() and video.flag is None:
                found_videos.append(video)

        if len(found_videos) == 0:
            print(f"No search results for {search_term}")
            return

        print(f"Here are the results for {search_term}:")
        for i, video in enumerate(found_videos, start=1):
            print(f"\t{i}) {video})")

        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")

        user_input = input()

        try:
            num = int(user_input)
        except ValueError:
            num = 0

        if 0 < num <= len(found_videos):
            self.play_video(found_videos[num-1].video_id)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        all_videos = sorted(self._video_library.get_all_videos(), key=operator.attrgetter("title"))
        found_videos = []
        for video in all_videos:
            if video_tag.lower() in video.tags and video.flag is None:
                found_videos.append(video)

        if len(found_videos) == 0:
            print(f"No search results for {video_tag}")
            return

        print(f"Here are the results for {video_tag}:")
        for i, video in enumerate(found_videos, start=1):
            print(f"\t{i}) {video})")

        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")

        user_input = input()

        try:
            num = int(user_input)
        except ValueError:
            num = 0

        if 0 < num <= len(found_videos):
            self.play_video(found_videos[num-1].video_id)

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)

        if video is None:
            print("Cannot flag video: Video does not exist")
        else:
            if video.flag is None:
                if self._playing_video == video.video_id:
                    self.stop_video()

                video.set_flag(flag_reason)
                print(f"Successfully flagged video: {video.title} (reason: {video.flag})")
            else:
                print("Cannot flag video: Video is already flagged")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)

        if video is None:
            print("Cannot remove flag from video: Video does not exist")
        else:
            if video.flag is None:
                print(f"Cannot remove flag from video: Video is not flagged")
            else:
                video.set_flag(None)
                print(f"Successfully removed flag from video: {video.title}")

