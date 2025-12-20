import time
from app.models.intersection import Intersection
from app.models.road import Road
from app.models.traffic_controller import TrafficController
from app.models.enums import Direction


def print_intersection_status(intersection: Intersection, controller: TrafficController, time_step: int):
    print(f"\nTime: {time_step}s")
    for direction in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
        road = intersection.get_road(direction)
        if road:
            traffic_light = road.get_traffic_light()
            if traffic_light:
                status_icon = {"RED": "🔴", "YELLOW": "🟡", "GREEN": "🟢"}
                status_value = traffic_light.get_status().value
                remaining = traffic_light.get_remaining_duration()
                print(f"{direction.value}: {status_icon.get(status_value, '⚪')} ({remaining}s)")


def demo():
    print("\n=== Traffic Signal Control System Demo ===")
    intersection = Intersection("MG_ROAD_INTERSECTION")

    north_road = Road("MG_ROAD_NORTH", Direction.NORTH, num_lanes=2)
    south_road = Road("MG_ROAD_SOUTH", Direction.SOUTH, num_lanes=2)
    east_road = Road("BRIGADE_ROAD_EAST", Direction.EAST, num_lanes=2)
    west_road = Road("BRIGADE_ROAD_WEST", Direction.WEST, num_lanes=2)

    intersection.add_road(north_road)
    intersection.add_road(south_road)
    intersection.add_road(east_road)
    intersection.add_road(west_road)

    controller = TrafficController(intersection)

    for t in range(70):
        controller.tick(t)
        if t % 10 == 0:
            print_intersection_status(intersection, controller, t)
            time.sleep(0.3)

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
