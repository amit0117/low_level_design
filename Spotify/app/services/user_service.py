from app.models.user import User
from app.models.artist import Artist


class UserService:

    @property
    def music_service_instance(self):
        from app.services.music_streaming_system import MusicStreamingSystem
        return MusicStreamingSystem.get_instance()

    def register_user(self, user: User):
        # Check if the current user is already present
        if user.id in self.music_service_instance.users:
            print("User already registered")
            return  # User is already registered

        # Use lock of MusicStreamingSystem
        with self.music_service_instance._lock:
            self.music_service_instance.users[user.id] = user

    def remove_user(self, user: User):
        if user.id not in self.music_service_instance.users:
            print("User not found")
            return  # User is not registered

        with self.music_service_instance._lock:
            del self.music_service_instance.users[user.id]

    def register_artist(self, artist: Artist):
        if artist.id in self.music_service_instance.artists:
            print("Artist already registered")
            return  # Artist is already registered
        with self.music_service_instance._lock:
            self.music_service_instance.artists[artist.id] = artist

    def remove_artist(self, artist: Artist):
        if artist.id not in self.music_service_instance.artists:
            print("Artist not found")
            return  # Artist is not registered
        with self.music_service_instance._lock:
            del self.music_service_instance.artists[artist.id]
