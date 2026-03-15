"""
Mermaid Diagrams for CricInfo (Cricket Management) - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    CricInfoService[CricInfoService] -->|manages| MatchService[MatchService]
    MatchService -->|creates| Match[Match Subject]

    Team[Team] -->|has many| Player[Player]
    Player -->|has| PlayerStats[PlayerStats]
    Player -->|has| PlayerRole[PlayerRole]

    Match -->|between| Team1[Team 1]
    Match -->|between| Team2[Team 2]
    Match -->|has| MatchType[MatchType]

    Match -->|has| MatchState{Match State}
    MatchState -->|scheduled| ScheduledState[ScheduledState]
    MatchState -->|live| LiveState[LiveState]
    MatchState -->|break| InBreakState[InBreakState]
    MatchState -->|finished| FinishedState[FinishedState]
    MatchState -->|abandoned| AbandonedState[AbandonedState]

    Match -->|has| Inning[Inning]
    Inning -->|contains| Ball[Ball]
    Ball -->|built via| BallBuilder[BallBuilder]
    Inning -->|contains| Wicket[Wicket]
    Wicket -->|built via| WicketBuilder[WicketBuilder]
    Ball -->|has| ExtraType[ExtraType]

    Match -->|has| Commentary[Commentary]
    Commentary -->|managed by| CommentaryService[CommentaryService]

    Match -->|observed by| MatchObserver{Match Observers}
    MatchObserver -->|scorecard| ScorecardDisplay[ScorecardDisplay]
    MatchObserver -->|notifications| UserNotifier[UserNotifier]
    MatchObserver -->|commentary| CommentaryManager[CommentaryManager]
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor Admin
    actor Viewer as Viewer/Fan
    participant CricInfo as CricInfoService
    participant MatchService
    participant Match
    participant Inning
    participant BallBuilder
    participant Scorecard as ScorecardDisplay
    participant Notifier as UserNotifier
    participant Commentary as CommentaryManager

    Admin->>CricInfo: Create teams & players
    Admin->>MatchService: Schedule match (Team A vs Team B)
    MatchService->>Match: Initialize match
    Note over Match: State = ScheduledState

    Viewer->>Match: Subscribe to match updates

    Admin->>Match: Start match
    Note over Match: State = LiveState
    Match->>Notifier: Notify match started
    Notifier-->>Viewer: Match has begun!

    loop Ball by Ball
        Admin->>BallBuilder: Record ball details
        BallBuilder->>Inning: Add ball to inning
        Inning->>Match: Update score

        Match->>Scorecard: Update scorecard display
        Match->>Commentary: Add ball commentary
        Match->>Notifier: Notify score update
        Notifier-->>Viewer: Live score update

        alt Wicket falls
            Admin->>Inning: Record wicket (WicketBuilder)
            Inning->>Match: Update wicket count
            Match->>Scorecard: Update scorecard
            Match->>Notifier: Wicket alert!
            Notifier-->>Viewer: Wicket notification
        end
    end

    alt Innings break
        Note over Match: State = InBreakState
        Match->>Notifier: Innings break
        Note over Match: State = LiveState (2nd innings)
    end

    Admin->>Match: End match
    Note over Match: State = FinishedState
    Match->>Scorecard: Final scorecard
    Match->>Notifier: Match result
    Notifier-->>Viewer: Final result & winner

    Viewer->>Scorecard: View full scorecard
    Scorecard-->>Viewer: Detailed match stats
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
