# Meeting Room Reservation
# Entity: Meeting, Room (available state, capacity, location), Bookinng (Cancelled, Ongoing, Scheduled),Employee,
# Reservation manager, Interval
# functionality: book room for meeting, check availability, manage booking, Recurring Meetings
# Need to send Notification to all of the participants (Observer pattern)
# Strategy Pattern (which meeting room to assign -> Nearest, First Match Found)
# State Pattern -> for a booking

from __future__ import annotations
from enum import StrEnum, auto
from threading import Lock, Thread
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from uuid import uuid4

datetime_format = "%Y-%m-%dT%H:%M:%S"


class MeetingStatus(StrEnum):
    SCHEDULED = auto()
    CANCELLED = auto()
    COMPLETED = auto()

    @classmethod
    def can_contribute_to_availability(cls, status: MeetingStatus) -> bool:
        return status != cls.COMPLETED


class Interval:
    def __init__(self, start_time: datetime, end_time: datetime):
        self.id = str(uuid4())
        self.start_time = start_time
        self.end_time = end_time

    def overlap(self, other_interval: Interval):
        return not (
            (self.end_time <= other_interval.start_time)
            or (self.start_time >= other_interval.end_time)
        )

    def __srt__(self):
        return f"Interval with start time: {self.start_time.strftime(datetime_format)}, end time : {self.end_time.strftime(datetime_format)}"


class MeetingObserver(ABC):
    @abstractmethod
    def notify_about_meeting(self, meeting: Meeting) -> None:
        raise NotImplementedError("Subclasses must implment this method")


class MeetingSubject:
    def __init__(self):
        self.observers: list[MeetingObserver] = []

    def add_to_observers(self, observer: MeetingObserver):
        self.observers.append(observer)

    def notify(self, meeting: Meeting):
        for observer in self.observers:
            observer.notify_about_meeting(meeting)


class Employee(MeetingObserver):
    def __init__(self, employee_id: int, name: str):
        self.id = employee_id
        self.name = name
        self.meeting_history: list[Meeting] = []

    def print_meeting_history(self, status: MeetingStatus | None = None):
        if not self.meeting_history:
            print(f"No Meeting has been scheduled for employee_id {self.id}")
            return

        for meeting in self.meeting_history:
            if status in (None, meeting.status):
                print(str(meeting))

    def notify_about_meeting(self, meeting: Meeting) -> None:
        print(f"User {self.name} has been Notified about \n {str(meeting)}")

    def add_meeting(self, meeting: Meeting):
        self.meeting_history.append(meeting)


class Room:
    def __init__(self, room_no: int, location: str, capacity: int):
        self.room_no = room_no
        self.location = location
        self.capacity = capacity
        self.meeting_history: list[Meeting] = []
        self._processing_lock = Lock()

    def is_available(self, interval: Interval, capacity: int = 0) -> bool:
        if capacity > self.capacity:
            return False

        if any(
            meeting.interval.overlap(interval)
            for meeting in self.meeting_history
            if MeetingStatus.can_contribute_to_availability(meeting.status)
        ):
            return False
        return True

    def print_meeting_history(self, status: MeetingStatus | None = None):
        if not self.meeting_history:
            print(f"There is no meeting scheduled in root no:{self.root_no}")
            return

        for meeting in self.meeting_history:
            if status in (None, meeting.status):
                print(str(meeting))

    def book_meeting(self, meeting: Meeting) -> bool:
        with self._processing_lock:
            if not self.is_available(meeting.interval):
                interval = meeting.interval
                print(
                    f"The interval, start_time: {interval.start_time.strftime(datetime_format)} to end_time: {interval.end_time.strftime(datetime_format)} has booked by some other meeting"
                )
                return False
            self.meeting_history.append(meeting)
            # also add this meeting to each participants meeting_history
            meeting.add_meeting_to_participants_history()
            return True

    def get_meeting_history(self):
        return self.meeting_history

    def get_meeting_id(self) -> int:
        return len(self.meeting_history) + 1


# Meeting
class Meeting(MeetingSubject):
    def __init__(
        self,
        meeting_id: int,
        organizer: Employee,
        interval: Interval,
        participants: list[Employee],
        room_no: int,
    ):
        MeetingSubject.__init__(self)
        self.meeting_id = meeting_id
        self.organizer = organizer
        self.participants = participants
        self.interval = interval
        self.room_no = room_no
        self.status: MeetingStatus | None = None

        for participant in self.participants:
            self.add_to_observers(participant)

        self.change_status(MeetingStatus.SCHEDULED)

    def get_participants(self) -> list[Employee]:
        return self.participants

    def __str__(self):
        return f"Meeting from: {self.interval.start_time.strftime(datetime_format)}, to: {self.interval.end_time.strftime(datetime_format)} with total participants as: {len(self.participants)} , status: {self.status} in room no :{self.room_no}"

    def change_status(self, status: MeetingStatus):
        self.status = status
        self.notify(self)

    def add_meeting_to_participants_history(self):
        for participant in self.participants:
            participant.add_meeting(self)

    def change_meeting_room(self, new_meeting_room: int) -> None:
        if new_meeting_room != self.room_no:
            self.room_no = new_meeting_room
            self.notify(self)


class SingletonMeta(type):
    _lock: Lock = Lock()
    _instances: dict[type, object] = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class MeetingRoomManager(metaclass=SingletonMeta):
    def __init__(self):
        self.employees: dict[int, Employee] = dict()
        self.rooms: dict[int, Room] = dict()
        self.meetings: dict[int, Meeting] = dict()

    def get_all_available_rooms(
        self, interval: Interval, capacity: int = 0
    ) -> list[int]:
        return [
            room.room_no
            for room in self.rooms.values()
            if room.is_available(interval, capacity)
        ]

    def print_all_available_room(self, interval: Interval) -> None:
        available_rooms = self.get_all_available_rooms(interval)
        if self.get_all_available_rooms(interval):
            print(
                f"Total available room for {str(interval)} is {len(available_rooms)}, [{",".join(available_rooms)}]"
            )
        else:
            print(f"No meeting room available for interval {str(interval)}")

    def book_meeting(
        self,
        organizer: Employee,
        start_time: datetime,
        end_time: datetime,
        participants: list[Employee],
    ) -> int | None:
        interval = Interval(start_time, end_time)
        available_rooms = self.get_all_available_rooms(interval, len(participants))
        # here we are assuming that we will pick the first available room for booking
        # if there is some way in which we want to consider the room for booking, we can implement a strategy Pattern
        # which will take the available_rooms and return the room (i.e based on location etc)

        if available_rooms:
            for room_no in available_rooms:
                room_to_book = self.rooms[room_no]
                meeting_id = room_to_book.get_meeting_id()
                meeting = Meeting(
                    meeting_id, organizer, interval, participants, room_to_book.room_no
                )
                if room_to_book.book_meeting(meeting):
                    print(
                        f"Meeting booked in room no: {room_to_book.room_no} by organizer: {organizer.name}"
                    )
                    self.meetings[meeting_id] = meeting

                    return meeting_id

        print("Couldn't book meeting")
        return None

    def cancel_meeting(self, meeting_id: int) -> None:
        if meeting_id not in self.meetings:
            print(f"No meeting found with meeting id: {meeting_id}")
            return

        meeting = self.meetings[meeting_id]
        meeting.change_status(MeetingStatus.CANCELLED)

    def print_meeting_history_for_employee(self, employee_id: int) -> None:
        if employee_id not in self.employees:
            print(f"No employee with employee_id {employee_id} found")
            return

        meeting_history = self.employees[employee_id]
        if not meeting_history:
            print(f"No meeting history for employee id {employee_id}")
            return

        for meeting in meeting_history:
            print(str(meeting))

    def print_meeting_history_for_room(self, room_no: int) -> None:
        if room_no not in self.rooms:
            print(f"No room with room no {room_no} found")
            return
        meeting_history = self.rooms[room_no]
        if not meeting_history:
            print(f"No meeting history for room no {room_no}")
            return

        for meeting in meeting_history:
            print(str(meeting))

    def add_employee(self, employee: Employee):
        self.employees[employee.id] = employee

    def add_room(self, room: Room) -> None:
        self.rooms[room.room_no] = room


if __name__ == "__main__":
    meeting_room_manager = MeetingRoomManager()
    room1 = Room(1, "first floor", 4)
    room2 = Room(2, "second floor", 3)
    room3 = Room(3, "Third Floor", 2)
    room4 = Room(4, "Fourch Floor", 1)

    for room in [room1, room2, room3, room4]:
        meeting_room_manager.add_room(room)

    # add employee
    emp1 = Employee(1, "Amit")
    emp2 = Employee(2, "Ankush")
    emp3 = Employee(3, "Rishu")
    emp4 = Employee(4, "Kushal")
    emp5 = Employee(5, "Vedansh")

    for emp in [emp1, emp2, emp3, emp4, emp5]:
        meeting_room_manager.add_employee(emp)

    start_time_1, end_time_1 = datetime.strptime(
        "2026-03-29T12:30:00", datetime_format
    ), datetime.strptime("2026-03-30T10:00:00", datetime_format)
    start_time_2, end_time_2 = datetime.strptime(
        "2026-03-30T09:30:00", datetime_format
    ), datetime.strptime("2026-03-30T15:00:00", datetime_format)

    meeting_1_id = meeting_room_manager.book_meeting(
        emp1, start_time_1, end_time_1, [emp1, emp2, emp3, emp4]
    )
    print("_" * 100, "\n")
    meeting_2_id = meeting_room_manager.book_meeting(
        emp2, start_time_2, end_time_2, [emp1, emp2, emp3]
    )

    # Cancel Meeting
    meeting_room_manager.cancel_meeting(meeting_1_id)
    print("_" * 100, "\n")
    meeting_room_manager.cancel_meeting(meeting_2_id)
    print("_" * 100, "\n")

    # Concurrent Booking

    def book_meeting(
        org: Employee,
        start_time: datetime,
        end_time: datetime,
        participants: list[Employee],
    ):
        meeting_room_manager.book_meeting(org, start_time, end_time, participants)
        print("_" * 150, "\n")

    thread1 = Thread(
        target=book_meeting,
        args=(emp1, start_time_1, end_time_1, [emp1, emp2, emp3, emp4]),
        name="first thread",
    )
    thread2 = Thread(
        target=book_meeting,
        args=(emp2, start_time_2, end_time_2, [emp1, emp2, emp3]),
        name="second thread",
    )
    thread3 = Thread(
        target=book_meeting,
        args=(
            emp3,
            start_time_1 + timedelta(hours=1),
            end_time_1 - timedelta(hours=1),
            [emp1, emp2, emp3, emp4],
        ),
        name="third thread",
    )
    thread4 = Thread(
        target=book_meeting,
        args=(emp4, start_time_1, end_time_1, [emp4]),
        name="fourth thread",
    )
    thread5 = Thread(
        target=book_meeting,
        args=(emp5, start_time_1, end_time_1, [emp1, emp5]),
        name="fifth thread",
    )

    # all_threads = [thread1, thread2, thread3, thread4, thread5]
    # for thread in all_threads:
    #     thread.start()

    # for thread in all_threads:
    #     thread.join()
