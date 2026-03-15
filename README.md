# 🎯 Low Level Design (LLD) - Complete Implementation Collection

A comprehensive collection of **25+ Low Level Design implementations** demonstrating advanced design patterns, clean architecture, SOLID principles, and enterprise-level software engineering practices.

## 📋 Table of Contents

- [Overview](#overview)
- [What is Low Level Design?](#what-is-low-level-design)
- [Projects by Difficulty](#projects-by-difficulty)
- [Design Patterns Covered](#design-patterns-covered)
- [Architecture Principles](#architecture-principles)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Learning Path](#learning-path)
- [Contributing](#contributing)

## 🎯 Overview

This repository contains **complete, production-ready implementations** of popular Low Level Design problems commonly asked in software engineering interviews.

Each project demonstrates:
- ✅ **Clean Architecture** - Separation of concerns, layered architecture
- ✅ **Design Patterns** - Creational, Structural, and Behavioral patterns
- ✅ **SOLID Principles** - Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- ✅ **Thread Safety** - Concurrent operations with proper locking
- ✅ **Type Safety** - Complete type hints throughout
- ✅ **Comprehensive Documentation** - Detailed README files for each project
- ✅ **Working Demos** - Executable demo scripts showcasing all features

## 🎓 What is Low Level Design?

**Low Level Design (LLD)** focuses on the detailed design of individual components, classes, and their interactions. It bridges the gap between High Level Design (system architecture) and actual code implementation.

### Key Aspects of LLD:

1. **Class Design** - Defining classes, their attributes, and methods
2. **Design Patterns** - Applying appropriate patterns to solve problems
3. **SOLID Principles** - Writing maintainable, extensible code
4. **Data Structures** - Choosing the right data structures for efficiency
5. **API Design** - Designing clean, intuitive interfaces
6. **Error Handling** - Robust exception handling and validation
7. **Thread Safety** - Handling concurrent operations correctly

## 📊 Projects by Difficulty

### 🟢 Easy Level Projects

Perfect for beginners to understand basic OOP concepts and simple design patterns.

| Project | Description | Key Patterns | README |
|---------|-------------|--------------|--------|
| **Parking Lot** | Design a parking lot system with multiple parking spots, vehicle types, and payment | Strategy, Factory | [README](parkingLot/README.md) |
| **Coffee Vending Machine** | Design a vending machine with inventory, payment, and dispensing | State, Observer, Factory | [README](coffeeVendingMachine/README.md) |
| **Logging Framework** | Design a logging system with multiple log levels and handlers | Chain of Responsibility, Strategy | [README](loggingFramework/readme.md) |
| **Traffic Signal System** | Design a traffic signal control system with multiple intersections | State, Strategy, Observer | [README](trafficSignalSystem/README.md) |
| **Tic Tac Toe** | Design a Tic Tac Toe game with player management and win detection | State, Observer | [README](ticTacToe/README.md) |
| **Task Management System** | Design a task management system with states, priorities, and assignments | State, Observer, Strategy, Builder, Repository | [README](taskManagementSystem/README.md) |

### 🟡 Medium Level Projects

Intermediate projects covering multiple design patterns and complex business logic.

| Project | Description | Key Patterns | README |
|---------|-------------|--------------|--------|
| **ATM System** | Design an ATM with card authentication, transaction processing, and cash dispensing | State, Command, Adapter, Factory | [README](atm/README.md) |
| **Library Management** | Design a library system with book lending, reservations, and fine calculation | Strategy, Factory, Observer, Repository | [README](libraryManagementService/README.md) |
| **Restaurant Management** | Design a restaurant system with table management, orders, and billing | State, Command, Decorator, Observer | [README](restrauntService/README.md) |
| **Elevator System** | Design an elevator system with floor requests, direction control, and scheduling | State, Strategy, Observer, Repository | [README](elevatorSystem/README.md) |
| **Pub-Sub System** | Design a publish-subscribe messaging system with topics and subscribers | Strategy, Factory, Observer, Repository | [README](pubSubService/README.md) |
| **Social Networking** | Design a social network with friend requests, posts, and news feed | Observer, Strategy, State, Repository | [README](socialNetworkingService/README.md) |
| **Online Auction** | Design an auction system with bidding, time-based closing, and notifications | State, Command, Mediator, Chain of Responsibility, Decorator | [README](onlineAuctionSystem/README.md) |
| **Airline Management** | Design an airline system with flight booking, seat selection, and pricing | State, Strategy, Observer, Decorator, Repository | [README](airlineManagementService/README.md) |
| **Online Stock Exchange** | Design a stock trading system with order matching and portfolio management | Observer, Strategy | [README](OnlineStockExchange/README.md) |

### 🔴 Hard Level Projects

Advanced projects with complex business logic, multiple subsystems, and sophisticated design patterns.

| Project | Description | Key Patterns | README |
|---------|-------------|--------------|--------|
| **Movie Ticket Booking** | Design a movie ticket booking system with seat selection, payment, and show management | Strategy, Observer, Repository | [README](movieTicketBookingService/README.md) |
| **Splitwise** | Design an expense splitting system with debt simplification and balance tracking | Strategy, Observer, Builder, Facade | [README](splitwise/README.md) |
| **Snake and Ladder** | Design a board game with dice rolling, player movement, and win conditions | State, Observer | [README](SnakeAndLadderGame/README.md) |
| **Online Shopping** | Design an e-commerce system with cart, checkout, payment, and inventory | Strategy, Observer, Factory | [README](onlineShoppingService/online_shopping_service_system.py) |
| **Ride Sharing (Uber)** | Design a ride-sharing system with driver matching, pricing, and trip management | Strategy, Observer, Decorator | [README](RideSharingService/README.md) |
| **CricInfo** | Design a cricket information system with match tracking, score updates, and statistics | Builder, Observer, State | [README](cricinfo/README.md) |
| **Spotify** | Design a music streaming service with playlists, recommendations, and playback | Strategy, Observer | [README](Spotify/run.py) |
| **UPI Payment System** | Design a UPI payment system with multiple banks, transaction processing, and security | Abstract Factory, Adapter, Chain of Responsibility, Command, Decorator, Proxy | [README](upi/README.md) |

## 🎨 Design Patterns Covered

### Creational Patterns
- ✅ **Singleton** - Single instance management (TaskManager, Repositories)
- ✅ **Factory** - Object creation (Payment factories, Vehicle factories)
- ✅ **Abstract Factory** - Families of related objects (UPI payment processors)
- ✅ **Builder** - Complex object construction (Task, Expense, Match)

### Structural Patterns
- ✅ **Adapter** - Interface adaptation (Payment adapters, Bank adapters)
- ✅ **Decorator** - Dynamic behavior extension (Price decorators, Feature decorators)
- ✅ **Proxy** - Access control and lazy loading (Payment proxies)
- ✅ **Facade** - Simplified interface to complex subsystems (Service facades)

### Behavioral Patterns
- ✅ **Observer** - Event-driven notifications (Task updates, Expense notifications)
- ✅ **Strategy** - Algorithm selection (Search strategies, Split strategies, Pricing strategies)
- ✅ **State** - State-based behavior (Task states, Payment states, Game states)
- ✅ **Command** - Encapsulate requests (ATM commands, Restaurant orders)
- ✅ **Chain of Responsibility** - Request processing chain (Payment processing, Logging)
- ✅ **Mediator** - Centralized communication (Auction mediator)
- ✅ **Repository** - Data access abstraction (Task repository, User repository)

## 🏗️ Architecture Principles

### SOLID Principles

All projects follow SOLID principles:

- **S**ingle Responsibility - Each class has one reason to change
- **O**pen/Closed - Open for extension, closed for modification
- **L**iskov Substitution - Subtypes must be substitutable for their base types
- **I**nterface Segregation - Clients shouldn't depend on interfaces they don't use
- **D**ependency Inversion - Depend on abstractions, not concretions

### Clean Architecture

Projects follow layered architecture:

```
┌─────────────────────────────────┐
│      Presentation/Demo Layer    │
│      (demo.py, run.py)          │
└─────────────────────────────────┘
              │
┌─────────────────────────────────┐
│         Service Layer           │
│    (Business Logic)             │
└─────────────────────────────────┘
              │
┌─────────────────────────────────┐
│      Repository Layer           │
│    (Data Access)                │
└─────────────────────────────────┘
              │
┌─────────────────────────────────┐
│        Domain Layer             │
│    (Models, Entities)           │
└─────────────────────────────────┘
              │
┌─────────────────────────────────┐
│    Strategy/Pattern Layer       │
│    (Design Patterns)            │
└─────────────────────────────────┘
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** - All projects are implemented in Python
- **Basic OOP Knowledge** - Understanding of classes, inheritance, polymorphism
- **Design Patterns** - Familiarity with common design patterns (optional, you'll learn as you go)

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd low_level_design
```

2. **Navigate to a project**
```bash
cd taskManagementSystem  # or any other project
```

3. **Run the demo**
```bash
python3 demo.py  # or run.py depending on the project
```

4. **Read the README**
Each project has a comprehensive README explaining:
- Architecture and design decisions
- Design patterns used
- How to run and use the system
- Code examples

### Project Structure

Each project follows a consistent structure:

```
projectName/
├── app/
│   ├── models/          # Domain entities
│   ├── services/        # Business logic
│   ├── repositories/     # Data access
│   ├── strategies/      # Strategy pattern implementations
│   ├── states/          # State pattern implementations
│   ├── observers/       # Observer pattern implementations
│   ├── builders/        # Builder pattern implementations
│   ├── factories/       # Factory pattern implementations
│   ├── commands/        # Command pattern implementations
│   ├── decorators/      # Decorator pattern implementations
│   └── ...
├── demo.py              # Demo script
├── run.py               # Alternative entry point
└── README.md            # Project documentation
```

## 📚 Learning Path (For LLD)


1.1 **Start with Easy Projects**
   - Parking Lot
   - Coffee Vending Machine
   - Tic Tac Toe
   - Task Management System

1.2 **Learn Basic Patterns**
   - Singleton
   - Factory
   - Strategy
   - Observer

1.3 **Understand SOLID Principles**
   - Read code comments
   - See how principles are applied
   - Try modifying code to see why design matters


2.1. **Tackle Medium Projects**
   - ATM System
   - Library Management
   - Elevator System
   - Pub-Sub System

2.2. **Explore Advanced Patterns**
   - State Pattern
   - Command Pattern
   - Chain of Responsibility
   - Repository Pattern

2.3. **Study Architecture**
   - Clean Architecture layers
   - Dependency Injection
   - Service Layer patterns


3.1. **Master Hard Projects**
   - Movie Ticket Booking
   - Splitwise
   - UPI Payment System
   - Ride Sharing Service

3.2. **Deep Dive into Complex Patterns**
   - Abstract Factory
   - Mediator
   - Multiple pattern combinations

3.3. **Optimize and Extend**
   - Add new features
   - Optimize performance
   - Add thread safety
   - Implement persistence

## 🎯 Key Learning Outcomes

After going through these projects, you will:

- ✅ **Master Design Patterns** - Understand when and how to apply 15+ design patterns
- ✅ **Write Clean Code** - Follow SOLID principles and clean architecture
- ✅ **Design Scalable Systems** - Build systems that can grow and evolve
- ✅ **Handle Concurrency** - Implement thread-safe operations
- ✅ **Think Like a Senior Engineer** - Make design decisions considering trade-offs
- ✅ **Ace Interviews** - Be prepared for LLD interviews at top tech companies

## 📖 How to Use This Repository

### 1. **Study Approach**
- Start with easy projects
- Read the README first
- Run the demo to see it in action
- Study the code structure
- Understand design decisions

### 2. **Practice Approach**
- Try to implement a project yourself first
- Compare with the solution
- Understand the differences
- Learn from the design choices

### 3. **Interview Preparation**
- Pick a problem statement
- Design the solution
- Implement it
- Compare with the solution here
- Understand trade-offs

## 🔍 Project Highlights

### Most Comprehensive Projects

1. **UPI Payment System** - 10+ design patterns, complex payment processing
2. **Task Management System** - Complete state management, search strategies, observer pattern
3. **Splitwise** - Advanced debt simplification algorithm, multiple split strategies
4. **Online Auction System** - Complex bidding logic, time-based events, mediator pattern

### Best for Learning Specific Patterns

- **Observer Pattern**: Task Management, Splitwise, Social Networking
- **State Pattern**: ATM, Elevator, Task Management, Traffic Signal
- **Strategy Pattern**: Parking Lot, Pub-Sub, Search systems
- **Builder Pattern**: Task Management, Splitwise, CricInfo
- **Command Pattern**: ATM, Restaurant Management, Online Auction
- **Chain of Responsibility**: UPI Payment, Logging Framework

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Add New Projects** - Implement new LLD problems
2. **Improve Documentation** - Enhance README files
3. **Fix Bugs** - Report and fix issues
4. **Add Features** - Extend existing projects
5. **Code Reviews** - Review and suggest improvements

### Contribution Guidelines

1. Follow the existing code structure
2. Add comprehensive documentation
3. Include working demo scripts
4. Follow SOLID principles
5. Add type hints
6. Write clean, readable code

## 🎓 Resources

### Recommended Reading

- [Head First Design Patterns](https://www.amazon.com/Head-First-Design-Patterns-Object-Oriented/dp/149207800X/)
- [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/B08X8ZXT15)
- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns)

### Online Resources

- [Refactoring Guru](https://refactoring.guru/) - Excellent design pattern explanations
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

## 📊 Statistics

- **25+ Projects** - Complete implementations
- **15+ Design Patterns** - Creational, Structural, Behavioral
- **1000+ Files** - Well-structured, documented code
- **SOLID Principles** - Applied throughout all projects
- **Thread Safety** - Concurrent operations handled correctly

## 🏆 Success Stories

This repository helps you:
- ✅ **Write Better Code** following industry best practices
- ✅ **Understand Design Patterns** through real-world implementations
- ✅ **Build Scalable Systems** with clean architecture
- ✅ **Think Like a Senior Engineer** making design decisions

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Review individual project READMEs
- Study the code and documentation

---

## 🌟 Star the Repository

If you find this repository helpful, please ⭐ star it to help others discover it!

---

**Made with ❤️ to help developers master Low Level Design and ace their interviews!**

**Happy Learning! 🚀**
