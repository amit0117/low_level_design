"""
Mermaid Diagrams for Spotify (Music Streaming) - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    User[User] -->|built via| UserBuilder[UserBuilder]
    User -->|follows| Artist[Artist Subject]
    User -->|creates| Playlist[Playlist]
    User -->|has| Subscription{Subscription}
    Subscription -->|free| Free[FREE]
    Subscription -->|premium| Premium[PREMIUM]

    Artist -->|releases| Album[Album]
    Album -->|contains| Song[Song]
    Song -->|has| Genre[SongGenre]
    Song -->|has| Theme[SongTheme]
    Song -->|implements| Playable[Playable Interface]
    Playlist -->|contains| Song

    Artist -->|notifies| ArtistObserver[ArtistObserver]
    ArtistObserver -->|updates| User

    User -->|loads playlist in| Player[Player]
    Player -->|has| PlayerState{Player State}
    PlayerState -->|playing| PlayingState[PlayingState]
    PlayerState -->|paused| PauseState[PauseState]

    Player -->|controlled via| Command{Command}
    Command -->|play| PlayCommand[PlayCommand]
    Command -->|pause| PauseCommand[PauseCommand]
    Command -->|stop| StopCommand[StopCommand]
    Command -->|next| NextTrackCommand[NextTrackCommand]
    Command -->|previous| PreviousTrackCommand[PreviousTrackCommand]
    Command -->|toggle| TogglePlayPauseCommand[TogglePlayPauseCommand]

    Player -->|uses| PlaybackStrategy{Playback Strategy}
    PlaybackStrategy -->|free| FreePlayback[FreePlaybackStrategy]
    PlaybackStrategy -->|premium| PremiumPlayback[PremiumPlaybackStrategy]

    User -->|gets suggestions from| RecommendationStrategy[RecommendationStrategy]
    RecommendationStrategy -->|genre based| GenreBased[GenreBasedRecommendationStrategy]

    User -->|searches via| SearchService[SearchService]
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor User
    participant UserBuilder
    participant Artist
    participant SearchService
    participant Playlist
    participant Player
    participant PlaybackStrategy
    participant RecommendationStrategy

    UserBuilder->>User: Build user profile
    User->>Artist: Follow artist
    Note over Artist: Observer pattern registered

    Artist->>Artist: Release new album
    Artist->>User: Notify new album available

    User->>SearchService: Search for songs
    SearchService-->>User: Search results

    User->>Playlist: Create playlist
    User->>Playlist: Add songs to playlist

    User->>Player: Load playlist
    Player->>PlaybackStrategy: Select strategy based on subscription

    alt FREE User
        PlaybackStrategy->>Player: FreePlaybackStrategy (with ads)
    else PREMIUM User
        PlaybackStrategy->>Player: PremiumPlaybackStrategy (ad-free)
    end

    User->>Player: PlayCommand
    Note over Player: State = PlayingState
    Player-->>User: Playing song

    User->>Player: NextTrackCommand
    Player-->>User: Playing next song

    User->>Player: PauseCommand
    Note over Player: State = PauseState

    User->>Player: TogglePlayPauseCommand
    Note over Player: State = PlayingState

    User->>RecommendationStrategy: Get recommendations
    RecommendationStrategy-->>User: Recommended songs by genre

    User->>Player: StopCommand
    Note over Player: Playback stopped
```
"""

if __name__ == "__main__":
    print("=" * 60)
    print("DATA FLOW DIAGRAM")
    print("=" * 60)
    print(DATA_FLOW_DIAGRAM)
    print("=" * 60)
    print("USER FLOW DIAGRAM")
    print("=" * 60)
    print(USER_FLOW_DIAGRAM)
