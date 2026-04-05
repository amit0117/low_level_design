from __future__ import annotations
from enum import StrEnum, auto
from threading import Condition, Thread
from abc import ABC
import time


class PersonOrRoomType(StrEnum):
    DEMOCRAT = auto()
    REPUBLICAN = auto()


class Person(ABC):
    def __init__(self, person_type: PersonOrRoomType, name: str) -> None:
        self.person_type = person_type
        self.name = name

    def __str__(self):
        return f"Name: {self.name} ,type: {self.person_type}"


class Democrat(Person):
    def __init__(self, name: str):
        super().__init__(PersonOrRoomType.DEMOCRAT, name)


class Republican(Person):
    def __init__(self, name: str):
        super().__init__(PersonOrRoomType.REPUBLICAN, name)


class BathroomScheduler:
    def __init__(self, max_room=3):
        self.max_room = max_room
        self.condition_variable = Condition()
        self.curr_person_type: PersonOrRoomType | None = None
        self.curr_room_used = 0

    def _get_time_by_person_name(self, name: str) -> int:
        # this is a sample function which will decide how much time a person will spend in a room
        # use hash based + base time
        k = 5
        base_time = 1
        return hash(name) % k + base_time

    def should_person_wait(self, person: Person):
        person_type = person.person_type
        opposite_type = (
            PersonOrRoomType.DEMOCRAT
            if person_type == PersonOrRoomType.REPUBLICAN
            else PersonOrRoomType.REPUBLICAN
        )
        return (
            self.curr_person_type == opposite_type
            or self.curr_room_used == self.max_room
        )

    def _pre_process_after_entry(self, person_type: PersonOrRoomType):
        if self.curr_person_type is None:
            self.curr_person_type = person_type

        self.curr_room_used += 1
        # print(f"ENTER: {person_type}, count={self.curr_room_used}")

    def _post_process_after_task_complete(self, person_type: PersonOrRoomType):
        self.curr_room_used -= 1
        if self.curr_room_used == 0:
            self.curr_person_type = None
        self.condition_variable.notify_all()
        print(f"EXIT: {person_type}, count={self.curr_room_used}")

    def book_room(self, person: Person):
        person_type = person.person_type
        with self.condition_variable:
            self.condition_variable.wait_for(
                lambda: not self.should_person_wait(person)
            )
            self._pre_process_after_entry(person_type)

        time_to_sleep = self._get_time_by_person_name(person.name)
        time.sleep(time_to_sleep)

        with self.condition_variable:
            self._post_process_after_task_complete(person_type)


def run_test():
    scheduler = BathroomScheduler(max_room=3)

    people = [
        Democrat("Democrat1"),
        Democrat("Democrat2"),
        Republican("Republican1"),
        Republican("Republican2"),
        Republican("Republican3"),
        Republican("Republican4"),
        Democrat("Democrat3"),
        Democrat("Democrat4"),
        Democrat("Democrat5"),
        Democrat("Democrat6"),
        Democrat("Democrat7"),
        Republican("Republican5"),
        Republican("Republican6"),
        Democrat("Democrat8"),
        Republican("Republican7"),
        Republican("Republican8"),
    ]

    threads = []

    for person in people:
        t = Thread(target=scheduler.book_room, args=(person,))
        threads.append(t)

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all to complete
    for t in threads:
        t.join()

    print("All people have used the bathroom.")


if __name__ == "__main__":
    run_test()
