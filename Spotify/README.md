# 🎵 Spotify - Music Streaming Service

A comprehensive music streaming service implementation demonstrating various design patterns and architectural principles. This project showcases a complete end-to-end music streaming system with user management, artist following, song playback, playlists, albums, search functionality, and personalized recommendations.

## 🚀 Features

### Core Functionality

- **User Management** - User registration, subscription management (Free/Premium)
- **Artist Management** - Artist profiles with album releases
- **Music Catalog** - Songs, Albums, and Playlists management
- **Playback Control** - Play, pause, stop, next, previous with state management
- **Playlist Management** - Create and manage custom playlists
- **Album Management** - Artist albums with track collections
- **Search Functionality** - Search songs by title, artist name, and search artists
- **Recommendations** - Personalized song recommendations based on genre
- **Observer Notifications** - Real-time notifications for album releases
- **Command Pattern** - Encapsulated playback commands for undo/redo support
- **Strategy Pattern** - Different playback strategies for Free vs Premium users

### Advanced Features

- **Subscription-based Playback** - Free users get ads every 3 songs, Premium users get ad-free experience
- **State Management** - Player state transitions (Stopped → Playing → Paused)
- **Observer Pattern** - Real-time notifications when artists release new albums
- **Builder Pattern** - Flexible user creation with UserBuilder
- **Command Pattern** - Playback commands with execute functionality
- **Strategy Pattern** - Flexible recommendation and playback strategies

### Design Patterns Implemented

- **Singleton Pattern** - Single instance of MusicStreamingSystem
- **Observer Pattern** - Real-time notifications for album releases
- **State Pattern** - Player state management (Stopped → Playing → Paused)
- **Strategy Pattern** - Playback strategies (Free vs Premium) and recommendation strategies
- **Command Pattern** - Playback commands (Play, Pause, Stop, Next, Previous, Toggle)
- **Builder Pattern** - User creation with UserBuilder
- **Facade Pattern** - MusicStreamingSystem as simplified interface
- **Repository Pattern** - Clean data access layer
- **Service Pattern** - Business logic separation

## 📁 Project Structure

```
Spotify/
├── app/
│   ├── models/
│   │   ├── artist_observer.py        # Observer pattern for artists
│   │   ├── artist.py                  # Artist model with observer
│   │   ├── command.py                 # Command pattern for playback
│   │   ├── enums.py                   # Enumerations
│   │   ├── person.py                  # Base Person class
│   │   ├── playable.py                # Playable interface (Song, Album, Playlist)
│   │   ├── playback_strategy.py       # Playback strategy pattern
│   │   ├── player.py                  # Player with state management
│   │   ├── player_states.py           # Player state pattern
│   │   ├── recommendation_strategy.py # Recommendation strategy
│   │   └── user.py                    # User model with builder
│   ├── services/
│   │   ├── music_streaming_system.py  # Main system (Singleton/Facade)
│   │   ├── recommendation_service.py # Recommendation service
│   │   ├── search_service.py          # Search functionality
│   │   └── user_service.py           # User management service
├── run.py                             # Demo script
└── README.md                          # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup Instructions

1. **Navigate to the Spotify directory**

   ```bash
   cd low_level_design/Spotify
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Run the demo**

   ```bash
   python run.py
   ```

## 🎯 Usage

### Running the Demo

The `run.py` file contains a comprehensive demonstration of all features:

```bash
python run.py
```

### Demo Sections

The demo includes comprehensive sections:

1. **User Registration** - Create Free and Premium users
2. **Artist Following** - Users follow artists
3. **Song Creation** - Create songs with artists, genres, and themes
4. **Album Creation** - Artists release albums
5. **Observer Pattern** - Real-time album release notifications
6. **Playlist Management** - Create and manage playlists
7. **Playback Control** - Play, pause, stop, next, previous commands
8. **Subscription-based Playback** - Free users get ads, Premium users don't
9. **Search Functionality** - Search songs and artists
10. **Recommendations** - Genre-based song recommendations

### Key Features Demonstrated

- **Subscription Tiers**: Free users get ads every 3 songs, Premium users get ad-free experience
- **Real-time Notifications**: Observer pattern delivers instant album release updates
- **State Management**: Player status follows proper state transitions
- **Command Pattern**: Encapsulated playback operations
- **Strategy Pattern**: Different playback behaviors for different subscription tiers
- **Search & Discovery**: Flexible search by title and artist name

## 📊 Entity Relationship Diagram

### Core Entities and Relationships

```
┌─────────────────────────────────────┐
│   MusicStreamingSystem              │
│─────────────────────────────────────│
│ (Singleton)                         │
│ - users (Dict<User>)                │
│ - artists (Dict<Artist>)            │
│ - songs (Dict<Song>)                │
│ - player (Player)                   │
│ - recommendation_service            │
│ - search_service                    │
│ - user_service                      │
└──────┬──────────────────────────────┘
       │
       │ 1..* (manages)
       │
       ▼
┌───────────────────────────────────────┐
│            User                       │
│───────────────────────────────────────│
│ id                                    │
│ name                                  │
│ email                                 │
│ address                               │
│ subscription_tier (UserSubscription)  │
│ followed_artists (Set<Artist>)        │
│ playback_strategy (PlaybackStrategy)  │
└──────┬────────────────────────────────┘
       │
       │ Inheritance from Person
       │
       ▼
┌─────────────────────────────────────┐
│          Person                     │
│─────────────────────────────────────│
│ id                                  │
│ name                                │
│ address                             │
│ email                               │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┐
       ▼              ▼
┌─────────────┐ ┌─────────────┐
│    User     │ │   Artist    │
└─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│          Artist                     │
│─────────────────────────────────────│
│ id                                  │
│ name                                │
│ albums (List<Album>)                │
│ subject (Subject)                   │
│ observers (List<Observer>)          │
└──────┬──────────────────────────────┘
       │
       │ 1..* (creates)
       │
       ▼
┌─────────────────────────────────────┐
│           Album                     │
│─────────────────────────────────────│
│ id                                  │
│ title                               │
│ tracks (List<Song>)                 │
└──────┬──────────────────────────────┘
       │
       │ 1..* (contains)
       │
       ▼
┌─────────────────────────────────────┐
│            Song                     │
│─────────────────────────────────────│
│ id                                  │
│ title                               │
│ duration                            │
│ artist (Artist)                     │
│ genre (SongGenre)                   │
│ theme (SongTheme)                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│          Playlist                   │
│─────────────────────────────────────│
│ id                                  │
│ title                               │
│ tracks (List<Song>)                 │
└─────────────────────────────────────┘

┌──────────────────────────────────────┐
│            Player                    │
│──────────────────────────────────────│
│ state (PlayerState)                  │
│ status (PlayerStatus)                │
│ queue (List<Song>)                   │
│ current_song (Song)                  │
│ current_index                        │
│ current_user (User)                  │
└──────┬───────────────────────────────┘
       │
       │ 1 (has)
       │
       ▼
┌─────────────────────────────────────┐
│        PlayerState                  │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┬──────────────┬
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Stopped    │ │  Playing    │ │   Paused    │
│   State     │ │   State     │ │   State     │
└─────────────┘ └─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│      PlaybackStrategy               │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┐
       ▼              ▼
┌─────────────┐ ┌─────────────┐
│   Free      │ │  Premium    │
│  Strategy   │ │  Strategy   │
└─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│          Command                    │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ PlayCommand │ │PauseCommand │ │StopCommand  │ │NextTrackCmd │ │PrevTrackCmd │ │ToggleCmd    │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

### Entity Relationships

1. **MusicStreamingSystem ↔ User** (One-to-Many)

   - System manages multiple Users
   - Users stored in dictionary

2. **MusicStreamingSystem ↔ Artist** (One-to-Many)

   - System manages multiple Artists
   - Artists stored in dictionary

3. **MusicStreamingSystem ↔ Song** (One-to-Many)

   - System manages multiple Songs
   - Songs stored in dictionary

4. **User ↔ Artist** (Many-to-Many via following)

   - A User can follow multiple Artists
   - An Artist can be followed by multiple Users

5. **Artist ↔ Album** (One-to-Many)

   - An Artist can release multiple Albums
   - Each Album belongs to one Artist

6. **Album ↔ Song** (One-to-Many)

   - An Album contains multiple Songs
   - A Song can be in multiple Albums

7. **Playlist ↔ Song** (Many-to-Many)

   - A Playlist contains multiple Songs
   - A Song can be in multiple Playlists

8. **Song ↔ Artist** (Many-to-One)

   - A Song is created by one Artist
   - An Artist can create multiple Songs

9. **Player ↔ User** (Many-to-One)

   - A Player can be used by multiple Users (sequentially)
   - Each playback session is for one User

10. **Player ↔ Song** (Many-to-Many via queue)

    - A Player has a queue of Songs
    - Songs can be played in different Players

11. **Player ↔ PlayerState** (One-to-One)

    - Each Player has one current State
    - State transitions: Stopped → Playing → Paused → Stopped

12. **User ↔ PlaybackStrategy** (One-to-One)

    - Each User has one PlaybackStrategy based on subscription
    - Free users get FreePlaybackStrategy, Premium users get PremiumPlaybackStrategy

13. **Observer Pattern Relationships**

    - Artist implements `Subject` - notifies on album releases
    - User (via Person) implements `ArtistObserver` - receives album release notifications

14. **Command Pattern Relationships**

    - Commands (PlayCommand, PauseCommand, etc.) encapsulate player operations
    - Commands execute operations on Player

15. **Strategy Pattern Relationships**
    - RecommendationService uses `RecommendationStrategy` (GenreBasedRecommendationStrategy)
    - User uses `PlaybackStrategy` (FreePlaybackStrategy or PremiumPlaybackStrategy)

## 🔄 Data Flow Diagrams

### 1. User Registration Flow

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     │ 1. UserBuilder.build()
     ▼
┌─────────────────┐
│   UserBuilder   │
│   (Builder)     │
└────┬────────────┘
     │
     │ 2. Create User
     │ 3. Set subscription
     ▼
┌─────────────────┐
│     User        │
└────┬────────────┘
     │
     │ 4. add_new_user()
     ▼
┌─────────────────┐
│MusicStreamingSys│
└────┬────────────┘
     │
     │ 5. user_service.register_user()
     ▼
┌─────────────────┐
│  UserService    │
└─────────────────┘
```

### 2. Album Release Flow

```
┌──────────┐
│  Artist  │
└────┬─────┘
     │
     │ 1. release_album(album)
     ▼
┌─────────────────┐
│     Artist      │
└────┬────────────┘
     │
     │ 2. Add album to albums list
     │ 3. subject.notify_observers()
     ▼
┌─────────────────┐
│     Subject     │
└────┬────────────┘
     │
     │ 4. Notify all observers
     ▼
┌─────────────────┐
│  All Observers  │
│  (Users)        │
└────┬────────────┘
     │
     │ 5. update(artist, album)
     ▼
┌─────────────────┐
│     Users       │
│  (Notified)     │
└─────────────────┘
```

### 3. Playback Flow

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     │ 1. Load playlist/album
     │ 2. Execute PlayCommand
     ▼
┌─────────────────┐
│  PlayCommand    │
│  (Command)      │
└────┬────────────┘
     │
     │ 3. execute()
     │ 4. player.click_play()
     ▼
┌─────────────────┐
│     Player      │
└────┬────────────┘
     │
     │ 5. state.play()
     │ 6. Get playback strategy
     ▼
┌─────────────────┐
│ PlaybackStrategy│
│  (Free/Premium) │
└────┬────────────┘
     │
     │ 7. Play song
     │ 8. Show ad (if Free, every 3 songs)
     │ 9. Update state to Playing
     ▼
┌─────────────────┐
│  PlayingState   │
└─────────────────┘
```

### 4. Search Flow

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     │ 1. search_songs_by_title(query)
     │    search_songs_by_artist_name(query)
     ▼
┌─────────────────┐
│MusicStreamingSys│
└────┬────────────┘
     │
     │ 2. search_service.search()
     ▼
┌─────────────────┐
│ SearchService   │
└────┬────────────┘
     │
     │ 3. Filter songs/artists
     │ 4. Return results
     ▼
┌─────────────────┐
│  Results        │
│  (Songs/Artists)│
└─────────────────┘
```

### 5. Recommendation Flow

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     │ 1. get_song_recommendations()
     ▼
┌─────────────────┐
│MusicStreamingSys│
└────┬────────────┘
     │
     │ 2. recommendation_service.recommend()
     ▼
┌─────────────────┐
│Recommendation   │
│   Service       │
└────┬────────────┘
     │
     │ 3. strategy.recommend()
     ▼
┌─────────────────┐
│Recommendation   │
│   Strategy      │
│  (GenreBased)   │
└────┬────────────┘
     │
     │ 4. Filter and rank songs
     │ 5. Return top recommendations
     ▼
┌─────────────────┐
│  Recommended    │
│     Songs       │
└─────────────────┘
```

### 6. Complete System Interaction Flow

```
┌──────────────┐
│   Client     │
│  (run.py)    │
└──────┬───────┘
       │
       │ All Operations
       ▼
┌─────────────────────────────────────┐
│   MusicStreamingSystem              │
│   (Singleton/Facade)                │
│  - User Management                  │
│  - Artist Management                │
│  - Song Management                  │
│  - Playback Control                 │
└──────┬──────────────────────────────┘
       │
       ├──────────────────┬──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌──────────────┐
│ UserService │  │SearchService│  │Recommendation│
│             │  │             │  │   Service    │
└─────────────┘  └─────────────┘  └──────────────┘
       │                  │                  │
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Users     │  │   Songs     │  │  Player     │
│  - Artists  │  │  - Albums   │  │  - State    │
│  - Strategy │  │  - Playlists│  │  - Queue    │
└─────────────┘  └─────────────┘  └─────────────┘
       │
       │
       ▼
┌───────────────────────────────────────┐
│         Pattern Layer                 │
│  - PlayerState (State)                │
│  - PlaybackStrategy (Strategy)        │
│  - RecommendationStrategy (Strategy)  │
│  - Commands (Command)                 │
│  - ArtistObserver (Observer)          │
└───────────────────────────────────────┘
```

## 📋 Entity Attributes Summary

### User Entity

- `id`: Unique identifier
- `name`: User's name
- `email`: User's email address
- `address`: User's address
- `subscription_tier`: UserSubscription (FREE, PREMIUM)
- `followed_artists`: Set of followed Artist objects
- `playback_strategy`: PlaybackStrategy object

### Artist Entity

- `id`: Unique identifier
- `name`: Artist name
- `albums`: List of Album objects
- `subject`: Subject object for observer pattern
- `observers`: List of Observer objects

### Song Entity

- `id`: Unique identifier
- `title`: Song title
- `duration`: Song duration
- `artist`: Reference to Artist
- `genre`: SongGenre (POP, CLASSICAL, ROCK)
- `theme`: SongTheme (HAPPY, SAD, DRAMATIC, ROMANTIC)

### Album Entity

- `id`: Unique identifier
- `title`: Album title
- `tracks`: List of Song objects

### Playlist Entity

- `id`: Unique identifier
- `title`: Playlist title
- `tracks`: List of Song objects

### Player Entity

- `state`: PlayerState object
- `status`: PlayerStatus (PLAYING, PAUSED, STOPPED)
- `queue`: List of Song objects
- `current_song`: Currently playing Song
- `current_index`: Index of current song in queue
- `current_user`: Currently active User

### PlayerState Entity (Abstract)

- `StoppedState`: Player is stopped
- `PlayingState`: Player is playing
- `PauseState`: Player is paused

### PlaybackStrategy Entity (Abstract)

- `FreePlaybackStrategy`: Shows ads every 3 songs
- `PremiumPlaybackStrategy`: Ad-free playback

### Command Entity (Abstract)

- `PlayCommand`: Play playback command
- `PauseCommand`: Pause playback command
- `StopCommand`: Stop playback command
- `NextTrackCommand`: Next track command
- `PreviousTrackCommand`: Previous track command
- `TogglePlayPauseCommand`: Toggle play/pause command

## 🏗️ Architecture

### Design Patterns

#### Singleton Pattern

- `MusicStreamingSystem` ensures single instance
- Thread-safe implementation with double-checked locking
- Centralized access point for all operations

#### Observer Pattern

- Real-time notifications for album releases
- Artist implements `Subject` - notifies followers
- User (via Person) implements `ArtistObserver` - receives notifications
- Decoupled notification system

#### State Pattern

- Player state management
- Proper state transitions (Stopped → Playing → Paused → Stopped)
- State-specific behavior changes

#### Strategy Pattern

- **Playback Strategies**:
  - `FreePlaybackStrategy`: Shows ads every 3 songs
  - `PremiumPlaybackStrategy`: Ad-free playback
- **Recommendation Strategies**:
  - `GenreBasedRecommendationStrategy`: Recommends songs based on genre
- Runtime strategy selection based on user subscription

#### Command Pattern

- Encapsulated playback operations
- Commands: Play, Pause, Stop, Next, Previous, Toggle
- Supports undo/redo functionality (extensible)

#### Builder Pattern

- `UserBuilder` for flexible user creation
- Fluent interface for setting user properties
- Validates user data before creation

#### Facade Pattern

- `MusicStreamingSystem` provides simplified interface
- Hides internal complexity of services
- Unified API for all operations

### Concurrency & Thread Safety

- **Thread-Safe Singletons**: Double-checked locking mechanism
- **Thread-Safe Collections**: Lock-based operations for shared data
- **State Management**: Thread-safe state transitions
- **Observer Notifications**: Thread-safe notification delivery

## 📊 Performance Metrics

The system demonstrates excellent performance characteristics:

- **User Registration**: Instant user creation
- **Song Addition**: Fast catalog management
- **Search Operations**: Efficient search algorithms
- **Playback Control**: Real-time state transitions
- **Observer Notifications**: Instant album release updates

## 🧪 Testing

The demo includes comprehensive testing covering:

- **User Management**: Registration and subscription management
- **Artist Following**: Follow/unfollow functionality
- **Album Releases**: Observer pattern validation
- **Playback Control**: All command operations
- **Subscription Tiers**: Free vs Premium playback behavior
- **Search Functionality**: Title and artist name search
- **Recommendations**: Genre-based recommendations

## 🔧 Configuration

### Subscription Tiers

```python
# Free users get ads every 3 songs
class FreePlaybackStrategy(PlaybackStrategy):
    def play(self, song: Song, player: Player):
        self.song_played += 1
        if self.song_played % 3 == 0:
            print("Showing ad for 1 sec")

# Premium users get ad-free experience
class PremiumPlaybackStrategy(PlaybackStrategy):
    def play(self, song: Song, player: Player):
        # No ads
        player.set_current_song(song)
```

### Recommendation Strategies

```python
# Genre-based recommendations
class GenreBasedRecommendationStrategy(RecommendationStrategy):
    def recommend(self, all_songs: list[Song]) -> list[Song]:
        # Return top 3 songs in same genre
        return filtered_songs[:3]
```

## 📈 Scalability

The system is designed for scalability:

- **Horizontal Scaling**: Service layer allows distribution
- **Vertical Scaling**: Efficient algorithms and data structures
- **Caching**: Observer pattern enables efficient notification caching
- **Load Balancing**: Stateless service design supports load balancing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is for educational purposes demonstrating design patterns and architectural principles.

## 🎓 Learning Objectives

This project demonstrates:

- **Design Patterns**: Singleton, Observer, State, Strategy, Command, Builder, Facade
- **Architecture**: Clean separation of concerns, layered architecture
- **Subscription Management**: Free vs Premium tier handling
- **Real-time Systems**: Observer pattern for instant notifications
- **Command Encapsulation**: Command pattern for playback operations
- **Best Practices**: Error handling, validation, documentation

## 🔍 Code Quality

- **Type Hints**: Full type annotation support
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Proper exception management
- **Validation**: Input validation and data integrity checks
- **Clean Code**: Readable, maintainable, and well-structured

## 🌟 Key Features Showcased

### Real-world Scenarios

- Complete music streaming workflow from registration to playback
- Subscription-based feature differentiation
- Real-time artist album release notifications
- Personalized song recommendations
- Flexible search and discovery

### Design Pattern Integration

- Multiple patterns working together seamlessly
- Clean separation of concerns
- Extensible and maintainable architecture
- Real-time notification system
- Command-based playback control

## 🚀 Advanced Features

### Subscription-based Playback

- **Free Users**: Ads every 3 songs, limited features
- **Premium Users**: Ad-free experience, full features
- **Strategy Selection**: Runtime strategy selection based on subscription

### Observer Notifications

- **Album Releases**: Users automatically notified when followed artists release albums
- **Decoupled System**: Artists don't need to know about users
- **Dynamic Subscription**: Users can follow/unfollow artists at runtime

### Command Pattern

- **Encapsulated Operations**: All playback operations are commands
- **Undo/Redo Support**: Extensible for undo/redo functionality
- **Command Queue**: Can queue commands for batch execution

### State Management

- **Player States**: Stopped, Playing, Paused states
- **State Transitions**: Proper state transition validation
- **State-specific Behavior**: Each state has specific behavior

---

**Note**: This is a demonstration project showcasing design patterns and architectural principles. For production use, additional considerations like database persistence, authentication security, API endpoints, payment processing, and streaming infrastructure would be required.
