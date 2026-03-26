# entities -> gate (entry, exit), vehicle (car, bike) , Enum (vehicle type)
# floor, parking spot (status as available , occupied)
# find available parking spot strategy -> first match
# pricing strategy -> vehicle type (max of base,time_taken*time_percost)
# payment strategy -> upi (strategy pattern)
# parking_lot manamegemnt service
# ticket ()
# Functional Requirement : park, unpark, search
# Non Functional requirement : thread safe

from __future__ import annotations
from enum import StrEnum,Enum,auto
from abc import ABC,abstractmethod
from threading import Lock
from datetime import datetime,timedelta

class VehicleType(Enum):

    CAR=("car",100,10) # vehicle_type, base_price, price_per_time / minute
    BIKE=("bike",50,5)

    def __init__(self,vehicle_type,base_price,price_per_time):
        self._vehicle_type=vehicle_type
        self._base_price=base_price
        self._price_per_time=price_per_time

    @property
    def vehicle_type(self):
        return self._vehicle_type

    @property
    def base_price(self):
        return self._base_price

    @property
    def price_per_time(self):
        return self._price_per_time

class ParkingSpotAvailabilityStatus(StrEnum):
    AVAILABLE=auto()
    OCCUPIED=auto()

class PaymentStatus(StrEnum):
    SUCCESS=auto()
    FAILED=auto()

class GateType(StrEnum):
    ENTRY=auto()
    EXIT=auto()

class Vehicle(ABC):
    def __init__(self,vehicle_type:VehicleType,number_plate:str):
        self._vehicle_type=vehicle_type
        self._number_plate=number_plate

    @property
    def vehicle_type(self):
        return self._vehicle_type

    @property
    def number_plate(self):
        return self._number_plate

class Car(Vehicle):
    def __init__(self,number_plate:str):
        super().__init__(VehicleType.CAR,number_plate)

class Bike(Vehicle):
    def __init__(self,number_plate):
        super().__init__(VehicleType.BIKE,number_plate)

class Gate(ABC):
    def __init__(self,gate_number:int,gate_type:GateType):
        self._gate_number=gate_number
        self._gate_type=gate_type

    @property
    def gate_number(self):
        return self._gate_number

    @property
    def gate_type(self):
        return self._gate_type

class EntryGate(Gate):
    def __init__(self,gate_number):
        super().__init__(gate_number,GateType.ENTRY)

class ExitGate(Gate):
    def __init__(self,gate_number):
        super().__init__(gate_number,GateType.EXIT)

class ParkingSpot:
    def __init__(self,spot_number,floor_number,vehicle_type):
        self._spot_number=spot_number
        self.floor_number=floor_number
        self._vehicle_type=vehicle_type
        self.status=ParkingSpotAvailabilityStatus.AVAILABLE
        self.lock=Lock()

    def is_available(self):
        return self.status==ParkingSpotAvailabilityStatus.AVAILABLE

    def park(self)->bool:
        if not self.is_available():
            print(f"Spot number {self.spot_number} at floor number {self.floor_number} is not available\n")
            return
        with self.lock:
            self.status=ParkingSpotAvailabilityStatus.OCCUPIED
        return True

    def unpark(self)->bool:
        if self.is_available():
            print(f"Spot numbe f{self.spot_number} at floor number {self.floor_number} is already unparked\n")
            return False

        with self.lock:
            self.status=ParkingSpotAvailabilityStatus.AVAILABLE
        return True


    @property
    def vehicle_type(self):
        return self._vehicle_type

    @property
    def spot_number(self):
        return self._spot_number

class Floor:
    def __init__(self,floor_number:int):
        self._floor_number=floor_number
        self.parking_spots:list[ParkingSpot]=[]

    def add_parking_spots(self,parking_spots:list[ParkingSpot]):
        self.parking_spots.extend(parking_spots)

    def available_spots(self,vehicle_type:VehicleType):
        # for bike we can park in cark parking spot as well
        allowed_vehicle_type=[vehicle_type]
        if vehicle_type== VehicleType.BIKE:
            allowed_vehicle_type.append(VehicleType.CAR)

        return [spot for spot in self.parking_spots if spot.vehicle_type in allowed_vehicle_type and spot.is_available()]

class Ticket:
    def __init__(self,ticket_number,entry_gate_number,vehicle,spot,floor_number):
        self.ticket_number=ticket_number
        self.entry_gate_number=entry_gate_number
        self.vehicle=vehicle
        self.parked_at=datetime.now()
        self.unparked_at=None
        self.exit_gate_number=None
        self.payment=None
        self.spot:Spot=spot
        self.floor_number=floor_number

    def parked_time_in_minutes(self):
        if not self.unparked_at:
            print(f"Ticket {self.ticket_number} is not found.\n")
            return

        total_parked_time_in_minutes=(self.unparked_at-self.parked_at)/timedelta(minutes=1)
        return total_parked_time_in_minutes

    def update_unpark_time(self):
        self.unparked_at=datetime.now()

    def update_exit_gate(self,exit_gate):
        self.exit_gate=exit_gate

    def update_payment(self,payment):
        self.payment=payment

class PaymentResponse:
    def __init__(self,payment_method,status:PaymentStatus,amount):
        self.method=payment_method
        self.status=status
        self.amount=amount

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        raise NotImplementedError("Subclasses must implement this class")

class DebitCard(PaymentMethod):

    # skipping the card details and the validation for now
    def pay(self,amount)->PaymentResponse:
        print(f"Making payment of amount {amount} using DebitCard\n")
        return PaymentResponse("DebitCard",PaymentStatus.SUCCESS,amount )

class SingetonMeta(type):
    _lock=Lock()
    _instance:dict[type,object]=dict()

    def __call__(cls,*args,**kwargs):
        if cls not in cls._instance:
            with cls._lock:
                if cls not in cls._instance:
                    cls._instance[cls]=super().__call__(*args,**kwargs)
        return cls._instance[cls]

class ParkingLotManager(metaclass=SingetonMeta):
    def __init__(self,total_floors:int,total_spot_per_floor:int=2):
        self.floors:dict[int,Floor]={floor_number:Floor(floor_number) for floor_number in range(1,total_floors+1)}
        self.tickets:dict[int,Ticket]=dict()
        self.exit_gates:dict[int,ExitGate]=dict()
        self.entry_gates:dict[int,EntryGate]=dict()
        self.total_spot_per_floor=total_spot_per_floor

        for floor in range(1,total_floors+1):
            self._initalize_single_floor(floor,self.total_spot_per_floor)

        # for simplicity create 1 entry and 1 exit_gate
        entry_gate=EntryGate(1)
        exit_gate=ExitGate(1)
        self.entry_gates[1]=entry_gate
        self.exit_gates[1]=exit_gate

    def _initalize_single_floor(self,floor_number,parking_spot_number=10):
        floor=self.floors[floor_number]
        mid=parking_spot_number//2
        # 1:5 car and 6:10 BIKE
        car_parking_spots=[ParkingSpot(spot_number,floor_number,VehicleType.CAR) for spot_number in range(1,mid+1)]
        bike_parking_spots=[ParkingSpot(spot_number,floor_number,VehicleType.BIKE) for spot_number in range(mid+1,parking_spot_number+1)]
        floor.add_parking_spots(car_parking_spots)
        floor.add_parking_spots(bike_parking_spots)

    # it should have park , unpark and search facility
    def available_spots(self,vehicle_type)->tuple[int,ParkingSpot]|None:

        for floor_number,floor in self.floors.items():
            available_spots=floor.available_spots(vehicle_type)
            if available_spots:
                return floor_number, available_spots[0]
        return None



    def park_vehicle(self,vehicle:Vehicle,gate_number):
        available_parking_spots=self.available_spots(vehicle.vehicle_type)

        if not available_parking_spots:
            print(f"No available parking spots found at gate_number {gate_number}, for vehicle_type {vehicle.vehicle_type}. So vehiche {vehicle.number_plate} can't parked\n")
            return


        # for now we are using the first available spots
        floor_number,spot=available_parking_spots

        # make as OCCUPIED
        if not spot.park():
           print(f"some other thread might have booked this spot {spot.spot_number}")
           return

        # mark spot as parked
        spot.park()

        ticket=Ticket(len(self.tickets),gate_number,vehicle,spot,floor_number)
        print(f"Vehicle {vehicle.number_plate} has parked at floor_number {ticket.floor_number} on spot_number {ticket.spot.spot_number}")
        return ticket

    def unpark_vehicle(self,ticket,exit_gate_number):
        exit_gate=self.exit_gates.get(exit_gate_number)
        if not exit_gate:
           print(f"Exit get for {exit_gate_number} not found\n")

        ticket.update_exit_gate(exit_gate_number)
        ticket.update_unpark_time()

        parked_time=ticket.parked_time_in_minutes()
        base_price=ticket.vehicle.vehicle_type.base_price
        price_per_time=ticket.vehicle.vehicle_type.price_per_time
        print(f"base price is {base_price}, price_per_time is {price_per_time}, parked_time is {parked_time}")
        total_amount=max(base_price ,price_per_time*parked_time)

        payment_method=DebitCard()
        payment=payment_method.pay(total_amount)

        ticket.update_payment(payment)
        spot=ticket.spot
        # mark the spot as empty
        if not spot.unpark():
            print("Not able to unpark vehicle")
            return

        print("unpark vehicle successfully")

    def search(self,vehicle_type):
        for floor_number, floor in self.floors.items():
            available_parking_spots=floor.available_spots(vehicle_type)
            print(f"Availbe parking spot for floor number {floor_number} is {len(available_parking_spots)}\n")

if __name__=="__main__":
    parking_lot_manager=ParkingLotManager(total_floors=2,total_spot_per_floor=2)
    car1=Car(number_plate="car1")
    car2=Car(number_plate="car2")
    car3=Car(number_plate="car3")
    bike1=Bike(number_plate="bike1")
    bike2=Bike(number_plate="bike2")
    bike3=Bike(number_plate="bike3")

    # search testing
    for vehicle_type in VehicleType:
        parking_lot_manager.search(vehicle_type)
    # park testing
    # parking car1 and bike1
    ticket1=parking_lot_manager.park_vehicle(car1,1)
    ticket2=parking_lot_manager.park_vehicle(bike1,1)

    # unpark testing (car1 and bike1 will be unparked)
    parking_lot_manager.unpark_vehicle(ticket1,1)
    parking_lot_manager.unpark_vehicle(ticket2,1)

    ticket3=parking_lot_manager.park_vehicle(car2,1)
    ticket4=parking_lot_manager.park_vehicle(car3,1)
