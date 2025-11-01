# Social Networking Service

A comprehensive social networking platform implementation demonstrating various design patterns and architectural principles. This project showcases a complete end-to-end social networking system with user management, friend connections, posts, likes, comments, notifications, and real-time features.

## 🚀 Features

### Core Functionality

- **User Registration & Authentication** - Secure user account creation and login
- **User Profiles** - Complete profile management with extensible structure
- **Friend Connections** - Send, accept, decline friend requests with state management
- **Posts & Newsfeed** - Create posts and view chronological feeds
- **Social Interactions** - Like and comment on posts with real-time tracking
- **Notifications** - Real-time notifications using Observer pattern
- **Privacy & Security** - Access control and data validation
- **Multi-User Concurrency** - Thread-safe operations with data consistency
- **Scalability** - High-performance design for large user bases

### Design Patterns Implemented

- **Singleton Pattern** - Single instance of SocialNetworkManager
- **Observer Pattern** - Real-time notifications for connections and interactions
- **State Pattern** - Connection request lifecycle management
- **Strategy Pattern** - Flexible feed generation and job recommendation algorithms
- **Repository Pattern** - Clean data access layer
- **Service Pattern** - Business logic separation
- **Facade Pattern** - Simplified interface to complex subsystem
- **Adapter Pattern** - Search engine abstraction (ElasticSearch/SQL)
- **Composite Pattern** - Hierarchical profile sections (Experience, Education, Skills)

### Domain Entities

| Domain Area                   | Key Entities                                                                   |
| ----------------------------- | ------------------------------------------------------------------------------ |
| **User & Profile**            | `User`, `Profile`, `Experience`, `Education`, `Skill`, `Connection`            |
| **Content & Interaction**     | `Post`, `Comment`, `Like`, `Share`, `Feed`                                     |
| **Messaging & Notifications** | `Message`, `Conversation`, `Notification`                                      |
| **Jobs & Recruitment**        | `Job`, `Company`, `Application`                                                |
| **System Infra**              | `FeedService`, `SearchService`, `RecommendationService`, `NotificationService` |

### Core Entities Overview

#### User Domain

- **User**: Main user entity with authentication, profile, and social connections
- **Profile**: Extended user profile with bio, location, and professional details
- **Experience**: Work experience entries with company, role, and duration
- **Education**: Educational background and qualifications
- **Skill**: User skills and endorsements
- **Connection**: Friend/follow relationships with state management

#### Content Domain

- **Post**: User-generated content with text, images, and metadata
- **Comment**: Threaded comments on posts and other commentable entities
- **Like**: User reactions to posts and comments
- **Share**: Content sharing functionality
- **Feed**: Personalized newsfeed for users

#### Communication Domain

- **Message**: Private messaging between users
- **Conversation**: Message threads and chat sessions
- **Notification**: Real-time alerts for social interactions

#### Professional Domain

- **Job**: Job postings and opportunities
- **Company**: Company profiles and information
- **Application**: Job applications and status tracking

#### Service Layer

- **FeedService**: Newsfeed generation and personalization
- **SearchService**: User and content search functionality
- **RecommendationService**: Content and connection suggestions
- **NotificationService**: Notification delivery and management

## 📁 Project Structure

```
socialNetworkingService/
├── run.py                          # Main demo file
├── social_network_manager.py       # Facade and Singleton implementation
├── app/
│   ├── models/                     # Domain models
│   │   ├── user.py                # User model with profile and connections
│   │   ├── post.py                # Post model (extends Commentable)
│   │   ├── commentable.py         # Abstract base for commentable entities
│   │   ├── like.py                # Like model
│   │   ├── comment.py             # Comment model
│   │   ├── connection.py          # Connection model
│   │   ├── notification.py        # Notification model
│   │   ├── profile.py             # User profile model
│   │   ├── job.py                 # Job, Company, Application models
│   │   └── enums.py               # Enum definitions
│   ├── services/                  # Business logic layer
│   │   ├── user_service.py        # User management service
│   │   ├── post_service.py        # Post management service
│   │   └── feed_service.py       # Newsfeed generation service
│   ├── repositories/              # Data access layer
│   │   ├── user_repository.py    # User data repository
│   │   └── post_repository.py    # Post data repository
│   ├── observers/                 # Observer pattern implementation
│   │   ├── connection_observer.py # Connection event observers
│   │   ├── commentable_observer.py # Commentable event observers
│   │   └── commentable_subject.py # Subject for commentable events
│   ├── states/                    # State pattern implementation
│   │   └── connection_state.py   # Connection state management
│   ├── strategies/                # Strategy pattern implementation
│   │   ├── feed_generation_strategy.py # Feed generation strategies
│   │   └── job_recommendation_strategy.py # Job recommendation strategies
│   └── exceptions/                # Custom exceptions
│       └── permission.py          # Permission-related exceptions
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd socialNetworkingService
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt  # If requirements.txt exists
   ```

4. **Run the demo**
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

The demo includes two main sections:

1. **Complete Social Networking Workflow** (9 scenarios)

   - User Registration & Login
   - Friend Request Management
   - Post Creation & Content Sharing
   - Social Interactions
   - Feed Generation Strategies
   - Notification System
   - Advanced Social Features
   - Edge Cases & Error Handling
   - Performance & Statistics

2. **Comprehensive Validation** (9 validation scenarios)
   - User Registration & Authentication
   - User Profiles
   - Friend Connections
   - Posts and Newsfeed
   - Likes and Comments
   - Privacy and Security
   - Notifications (Observer Pattern)
   - Multi-User Concurrency & Data Consistency
   - Scalability and Performance

### Key Features Demonstrated

- **Thread Safety**: Singleton pattern ensures single instance across threads
- **Real-time Notifications**: Observer pattern delivers instant notifications
- **Data Consistency**: Thread-safe operations prevent race conditions
- **State Management**: Connection requests follow proper state transitions
- **Feed Generation**: Chronological sorting with strategy pattern
- **Error Handling**: Comprehensive validation and error management

## 🔄 Data Flow

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FACADE LAYER                             │
│              SocialNetworkManager (Singleton)               │
│         (Simplified interface for all operations)           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   SERVICE LAYER                             │
│  UserService  │  PostService  │  FeedService                │
│  (Business Logic - User management, Posts, Feeds)           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                 REPOSITORY LAYER                            │
│ UserRepository │ PostRepository │ (Singleton Pattern)       │
│         (Data Access - Thread-safe operations)              │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   DOMAIN LAYER                              │
│   Models, States, Strategies, Observers, Subjects           │
│              (Business Entities & Behaviors)                │
└─────────────────────────────────────────────────────────────┘
```

### User Registration Flow

```
User Input → SocialNetworkManager → UserService → UserRepository → User Model
     ↓
Profile Creation → Account Setup → Notification Setup → Observer Registration
```

### Friend Connection Flow

```
User A sends request → UserService → Connection Model → State Management
     ↓
Notification sent → Observer Pattern → User B receives notification
     ↓
User B accepts/rejects → State Transition → Connection Update → Mutual friend addition
```

### Post Creation Flow

```
User creates post → PostService → Post Model → CommentableSubject setup
     ↓
Post stored → PostRepository → User's post list updated
     ↓
Feed generation → FeedService → Strategy Pattern → Chronological sorting
```

### Social Interaction Flow (Like/Comment)

```
User interaction → PostService → Like/Comment Model → CommentableSubject notification
     ↓
Observer Pattern → Real-time notification → Post author notified
     ↓
Post statistics updated → Like/Comment counts updated
```

### Newsfeed Generation Flow

```
User requests feed → FeedService → Get user's friends → Collect friend posts
     ↓
Strategy Pattern → ChronologicalStrategy → Sort by timestamp
     ↓
Return top 10 posts → Display to user
```

### Multi-User Concurrency Flow

```
Multiple users → ThreadPoolExecutor → Concurrent operations
     ↓
Singleton Manager → Thread-safe repositories → Process locks
     ↓
Data consistency → Observer notifications → Real-time updates
```

### Observer Pattern Data Flow

```
Event Trigger (Like/Comment/Connection) → CommentableSubject/ConnectionSubject
     ↓
notify_observers() → Observer List → Individual Observer.on_event()
     ↓
Notification Creation → User Notification List → Real-time Display
```

## 🏗️ Architecture

### Design Patterns

#### Singleton Pattern

- `SocialNetworkManager` ensures single instance
- Thread-safe implementation with double-checked locking
- Centralized access point for all operations

#### Observer Pattern

- Real-time notifications for connections and interactions
- Decoupled notification system
- Automatic event propagation

#### State Pattern

- Connection lifecycle management
- Proper state transitions (NotRequested → Pending → Accepted/Rejected)
- Invalid transition prevention

#### Strategy Pattern

- **Feed Generation Strategies**:

  - `ChronologicalStrategy`: Shows posts in reverse chronological order (most recent first)
  - `EngagementBasedStrategy`: Prioritizes posts with high user engagement (likes + comments)
  - `InterestBasedStrategy`: Recommends posts based on user's interests and past engagement
  - `PopularityBasedStrategy`: Shows most popular posts across the network
  - `MixedStrategy`: Combines multiple strategies for balanced recommendations

- **Job Recommendation Strategies**:

  - `SkillBasedStrategy`: Matches jobs based on user's skills and job requirements
  - `LocationBasedStrategy`: Prioritizes jobs in user's preferred location
  - `CompanyBasedStrategy`: Recommends jobs from companies where user's connections work
  - `SalaryBasedStrategy`: Shows jobs within user's expected salary range
  - `RecentJobsStrategy`: Displays most recently posted job opportunities

- Easy to add new strategies
- Runtime algorithm selection

#### Repository Pattern

- Clean data access layer
- Thread-safe data operations
- Separation of concerns

#### Service Pattern

- Business logic encapsulation
- Input validation and error handling
- Clean API interfaces

#### Facade Pattern

- Simplified interface to complex subsystem
- Hides internal complexity
- Unified API for all operations

#### Adapter Pattern

- **Search Engine Abstraction**: Translates between different search interfaces
- **ElasticSearch Integration**: Adapts ElasticSearch API to common search interface
- **SQL Fallback Support**: Allows switching between search engines seamlessly
- **Example Use Case**: `ProfileSearch` interface with `ElasticSearchAdapter` and `SQLSearchAdapter`

```python
# Common search interface
class ProfileSearch:
    def search(self, query: str) -> list:
        pass

# ElasticSearch adapter
class ElasticSearchAdapter(ProfileSearch):
    def search(self, query: str) -> list:
        # ElasticSearch specific implementation
        return elasticsearch_client.search(query)

# SQL fallback adapter
class SQLSearchAdapter(ProfileSearch):
    def search(self, query: str) -> list:
        # SQL implementation
        return db.query("SELECT * FROM profiles WHERE bio ILIKE ?", [f"%{query}%"])
```

#### Composite Pattern

- **Hierarchical Profile Structure**: Manages nested profile sections uniformly
- **Profile Components**: Experience, Education, Skills treated as ProfileComponent
- **Uniform Interface**: Same operations for leaf nodes (Skill) and composites (Experience)
- **Dynamic Composition**: Add/remove profile sections at runtime

```python
# Component interface
class ProfileComponent:
    def show(self, indent: int = 0) -> None:
        pass

# Leaf: Individual skill
class Skill(ProfileComponent):
    def show(self, indent: int = 0) -> None:
        print("  " * indent + f"Skill: {self.name}")

# Composite: Experience section containing skills
class ProfileSection(ProfileComponent):
    def __init__(self, title: str):
        self.title = title
        self.children: list[ProfileComponent] = []

    def add(self, component: ProfileComponent) -> None:
        self.children.append(component)

    def show(self, indent: int = 0) -> None:
        print("  " * indent + f"{self.title}:")
        for child in self.children:
            child.show(indent + 1)
```

### Use Cases for Composite Pattern

- **Profile Rendering**: Export profiles to PDF/HTML with uniform traversal
- **Profile Versioning**: Compare entire profile hierarchies
- **Dynamic Profile Sections**: Add custom sections like Projects, Certifications

### Job Recommendation Strategies

The system implements multiple strategies for job recommendations to provide personalized job suggestions:

#### Skill-Based Strategy

```python
class SkillBasedStrategy(JobRecommendationStrategy):
    def recommend_jobs(self, user: User, available_jobs: List[Job]) -> List[Job]:
        user_skills = user.get_profile().get_skills()
        # Score jobs based on skill matches with job requirements
        # Higher score for jobs matching more user skills
        return top_matching_jobs[:10]
```

**Use Case**: Perfect for developers looking for jobs matching their technical skills.

#### Location-Based Strategy

```python
class LocationBasedStrategy(JobRecommendationStrategy):
    def recommend_jobs(self, user: User, available_jobs: List[Job]) -> List[Job]:
        user_location = user.get_profile().get_location()
        # Prioritize jobs in same city/location
        # Exact matches get highest priority
        return location_matching_jobs[:10]
```

**Use Case**: Ideal for users who prefer local job opportunities.

#### Company-Based Strategy

```python
class CompanyBasedStrategy(JobRecommendationStrategy):
    def recommend_jobs(self, user: User, available_jobs: List[Job]) -> List[Job]:
        friends_companies = get_companies_where_friends_work()
        # Recommend jobs from companies where connections work
        # Leverages network for job referrals
        return network_based_jobs[:10]
```

**Use Case**: Great for leveraging professional network for job referrals.

#### Salary-Based Strategy

```python
class SalaryBasedStrategy(JobRecommendationStrategy):
    def recommend_jobs(self, user: User, available_jobs: List[Job]) -> List[Job]:
        # Filter and sort jobs by salary range
        # Show highest paying opportunities first
        return highest_salary_jobs[:10]
```

**Use Case**: Useful for users focused on compensation packages.

#### Recent Jobs Strategy

```python
class RecentJobsStrategy(JobRecommendationStrategy):
    def recommend_jobs(self, user: User, available_jobs: List[Job]) -> List[Job]:
        # Sort by posting date (most recent first)
        return sorted_jobs_by_date[:10]
```

**Use Case**: Shows the latest job opportunities in the market.

### Concurrency & Thread Safety

- **Thread-Safe Singletons**: Double-checked locking mechanism
- **Repository Locks**: Process locks for data access operations
- **State Management**: Thread-safe state transitions
- **Observer Notifications**: Thread-safe notification delivery

## 📊 Performance Metrics

The system demonstrates excellent performance characteristics:

- **User Registration**: 5 users in ~0.000 seconds
- **Post Creation**: 3 posts in ~0.000 seconds
- **Feed Generation**: 2 feeds in ~0.000 seconds
- **Concurrent Operations**: 5/5 successful with ThreadPoolExecutor
- **Data Consistency**: Zero data corruption under concurrent access

## 🧪 Testing

The demo includes comprehensive testing covering:

- **Multi-User Concurrency**: ThreadPoolExecutor with 5 concurrent operations
- **Data Consistency**: Verification of data integrity under load
- **Observer Pattern**: Real-time notification delivery validation
- **State Management**: Connection state transition testing
- **Error Handling**: Invalid operation testing
- **Performance**: Bulk operation timing

## 🔧 Configuration

### Environment Variables

No environment variables required for basic operation.

### Customization

- Feed generation strategies can be easily extended
- Notification types can be added to the Observer pattern
- New connection states can be implemented
- Additional user profile fields can be added

## 📈 Scalability

The system is designed for scalability:

- **Horizontal Scaling**: Repository pattern allows database distribution
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

- **Design Patterns**: Singleton, Observer, State, Strategy, Repository, Service, Facade, Adapter, Composite
- **Advanced Strategy Patterns**: Multiple feed generation strategies (chronological, engagement-based, interest-based, popularity-based, mixed) and job recommendation strategies (skill-based, location-based, company-based, salary-based, recent jobs)
- **Architecture**: Clean separation of concerns, layered architecture
- **Concurrency**: Thread safety, data consistency, race condition prevention
- **Testing**: Comprehensive validation, multi-user scenarios
- **Performance**: Efficient algorithms, scalability considerations
- **Best Practices**: Error handling, validation, documentation

## 🔍 Code Quality

- **Type Hints**: Full type annotation support
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Proper exception management
- **Validation**: Input validation and data integrity checks
- **Thread Safety**: Concurrent access protection
- **Clean Code**: Readable, maintainable, and well-structured

---

**Note**: This is a demonstration project showcasing design patterns and architectural principles. For production use, additional considerations like database persistence, authentication security, and API endpoints would be required.
