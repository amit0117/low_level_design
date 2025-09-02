from app.services.music_streaming_system import MusicStreamingSystem
from app.models.user import User, UserBuilder, Address
from app.models.artist import Artist
from app.models.playable import Song, Playlist, Album
from app.models.command import (
    PlayCommand,
    PauseCommand,
    StopCommand,
    NextTrackCommand,
    PreviousTrackCommand,
    TogglePlayPauseCommand,
)
from app.models.enums import SongGenre, SongTheme, UserSubscription


class MusicApplication:
    # This class is for demonstration of Music Streaming System functionality
    def __init__(self):
        self.music_service = MusicStreamingSystem.get_instance()

    def run(self):
        # Example usage of the music streaming system
        player = self.music_service.get_player()
        user1_address = Address("123 Main St", "City", "State", "12345")
        user2_address = Address(
            "456 Another St", "Another City", "Another State", "67890"
        )

        user1 = (
            UserBuilder(User("id1"))
            .add_name("Amit")
            .add_email("amit@example.com")
            .add_address(user1_address)
            .add_subscription(UserSubscription.FREE)
            .build()
        )
        user2 = (
            UserBuilder(User("id2"))
            .add_name("Ankush")
            .add_email("user2@example.com")
            .add_address(user2_address)
            .add_subscription(UserSubscription.PREMIUM)
            .build()
        )
        all_users = [user1, user2]

        artist1 = Artist(id="1", name="Arijit Singh")
        user1.follow_artist(artist1)  # user1 follows artist1

        artist2 = Artist(id="2", name="Shreya Ghoshal")
        user2.follow_artist(artist2)  # user2 follows artist2

        artist3 = Artist(id="3", name="Lata Mangeshkar")
        for user in all_users:
            user.follow_artist(artist3)  # all users follow artist3

        song1 = Song(
            id="1",
            duration="5min",
            title="Ami Je Tomar",
            artist=artist1,
            genre=SongGenre.POP,
            theme=SongTheme.ROMANTIC,
        )
        song3 = Song(
            id="3",
            duration="4min",
            title="Lehra Do",
            artist=artist1,
            genre=SongGenre.POP,
            theme=SongTheme.ROMANTIC,
        )
        song4 = Song(
            id="4",
            duration="3min",
            title="Dola Re Dola",
            artist=artist2,
            genre=SongGenre.CLASSICAL,
            theme=SongTheme.DRAMATIC,
        )
        song5 = Song(
            id="5",
            duration="4min",
            title="Pyar Kiya To Darna Kya",
            artist=artist3,
            genre=SongGenre.CLASSICAL,
            theme=SongTheme.ROMANTIC,
        )
        song6 = Song(
            id="6",
            duration="5min",
            title="Tune O Rangeele",
            artist=artist3,
            genre=SongGenre.CLASSICAL,
            theme=SongTheme.ROMANTIC,
        )

        all_songs = [song1, song3, song4, song5, song6]

        # Create Album for distinct artists
        album1 = Album(id="1", title="Arijit Singh Hits")
        for song in [song1, song3]:
            album1.add_track(song)

        album2 = Album(id="2", title="Shreya Ghoshal Melodies")
        for song in [song1, song4]:
            album2.add_track(song)

        album3 = Album(id="3", title="Lata Mangeshkar Classics")
        for song in [song5, song6]:
            album3.add_track(song)

        # Create playList for user1 and user2
        playlist1 = Playlist(id="1", title="Amit's Favorites")
        playlist2 = Playlist(id="2", title="Ankush's Favorites")
        playlist1_songs = all_songs[:]
        playlist2_songs = all_songs[3:]

        # Add songs to playlist1
        for song in playlist1_songs:
            playlist1.add_track(song)

        # Add songs to playlist2
        for song in playlist2_songs:
            playlist2.add_track(song)

        # Add songs to the music service
        for song in all_songs:
            self.music_service.add_song(song)

        # Add users to the music service
        for user in all_users:
            self.music_service.add_new_user(user)

        # Add artists to the music service
        all_artists = [artist1, artist2, artist3]
        for artist in all_artists:
            self.music_service.add_new_artist(artist)

        # Release albums for artist1
        print("Observer Pattern Demo\n")
        artist1.release_album(album1)
        print("\n\n")
        artist3.release_album(album3)
        print("\n\n")

        # Simulate user commands
        play = PlayCommand(player=player)
        pause = PauseCommand(player=player)
        stop = StopCommand(player=player)
        next_track = NextTrackCommand(player=player)
        previous_track = PreviousTrackCommand(player=player)
        toggle_play_pause = TogglePlayPauseCommand(player=player)

        # Play for user1
        print("Playing for User 1:")
        player.load(user1, playlist1)
        play.execute()
        pause.execute()
        stop.execute()
        next_track.execute()
        play.execute()
        print("\n")
        next_track.execute()
        play.execute()  # This should print add
        next_track.execute()
        play.execute()  # This should not print ad as only 3 songs in playlist
        previous_track.execute()
        toggle_play_pause.execute()

        # Play for second User
        print("Playing for User 2:\n")
        player.load(user2, playlist2)
        play.execute()
        next_track.execute()
        play.execute()
        next_track.execute()
        play.execute()
        next_track.execute()
        # This will not cause any ads to be played
        play.execute()

        # Search Service Demo

        print("\n\nSearch Service Demo\n")
        search_results_by_title = self.music_service.search_songs_by_title("do")
        print(f"Search Results by Title 'do' is : {str(search_results_by_title)}")
        for song in search_results_by_title:
            print(f"Found song by title: {song.title}")

        search_results_by_artist = self.music_service.search_songs_by_artist_name(
            "Arijit Singh"
        )
        print(
            f"Search Results by Artist 'Arijit Singh' is : {str(search_results_by_artist)}"
        )
        for song in search_results_by_artist:
            print(f"Found song by artist: {song.title}")

        print("\n\nRecommendation Service Demo\n")
        recommended_songs = self.music_service.get_song_recommendations()
        print(f"Recommended songs for User 1: {str(recommended_songs)}")
        for song in recommended_songs:
            print(f" - {song.title}")


if __name__ == "__main__":
    application = MusicApplication()
    application.run()
