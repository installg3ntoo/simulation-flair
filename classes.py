from enum import Enum
from random import randint
import json


class Building:
    """
    Class that represents a building with floors and rooms.


    Attributes
    ----------
    floors : list
        List of floors in the building.

    Parameters
    -------
    number_of_floors : int
        Number of floors in the building.
    number_of_rooms : int
        Number of rooms in each floor.
    """
    def __init__(self,  number_of_floors = None, number_of_rooms = None):
        if number_of_rooms is None or number_of_floors is None:
            self.floors = []
        else:
            self.floors = [Floor(floor_number, number_of_rooms) for floor_number in range(number_of_floors)]
    
    def __str__(self):
        return f"Building with {len(self.floors)} floors"
    
    def load_previous_state(self):
        pass



class Floor:
    """
    Class that represents a floor in a building.


    Attributes
    ----------
    rooms : list
        List of rooms in the floor.
    number : int
        Floor number.
    """
    def __init__(self, floor_number : int, number_of_rooms = None):
        if number_of_rooms is None:
            self.rooms = []
        else:
            self.rooms = [Room(i, self) for i in range(number_of_rooms)]

        self.number = floor_number

class Room:
    """
    Class that represents a room in a building.


    Attributes
    ----------
    floor : Floor
        Floor where the room is located.
    sensor : Sensor
        Sensor that detects zombies in the room.
    has_zombies : bool
        True if the room has zombies, False otherwise.
    blocked : bool
        True if the room is blocked, False otherwise.
    number : int
        Room number.
    visited : bool
        True if the room has been visited in the current iteration (for simulation).
    """
    def __init__(self, number : int, floor : Floor):

        self.floor = floor
        self.sensor = Sensor(self)
        self._has_zombies = False
        self.blocked = False
        self.number = number
        self.visited = False
    
    @property
    def has_zombies(self):
        return self._has_zombies
    
    @has_zombies.setter
    def has_zombies(self, value):
        if not self.sensor.state == State.OFF:
            if value:
                self.sensor.state = State.ALERT
            else:
                self.sensor.state = State.ON
        self._has_zombies = value


class State(Enum):
    ALERT = 2
    ON = 1
    OFF = 0

class Sensor:
    all = []
    count = 0

    def __init__(self, room):

        self.id = Sensor.count
        Sensor.count += 1
        self.room = room
        self.state = State.ON
        Sensor.all.append(self)

    def activate(self):
        if self.room.has_zombies:
            self.state = State.ALERT
        else:
            self.state = State.ON
    
    def deactivate(self):
        self.state = State.OFF
    
    def reset(self):
        self.state = State.ON
    
    def update(self):
        if self.state == State.ON and self.room.has_zombies:
            self.state = State.ALERT
        elif self.state == State.ALERT and not self.room.has_zombies:
            self.state = State.ON

    def __str__(self):
        return f"Sensor {self.id} at floor {self.room.floor.number} room {self.room.number} is {self.state.name}"
    

class Simulation:
    """
    Class that represents the full simulation.


    Attributes
    ----------
    building : Building
        Building with floors and rooms.
    time : int
        Time elapsed in the simulation.
    
        
    Methods
    -------
    add_zombies(floor_number, room_number): 
        Adds zombies to a given room from an specific floor.
    block_room(floor_number, room_number)
        Blocks a given room making zombies unable to leave or enter the room.
    print_state()
        Prints the state of all sensors.
    update_sensors()
        Updates the state of all sensors. (needed when resetting a sensor)
    reset_sensor(floor_number, room_number)
        Resets a given sensor from a given room in a given floor to state ON.
    update()
        Moves zombies to adjacent rooms and updates the simulation and sensors.
    save(path)
        Saves the simulation to a file.
    load(path)
        Loads a simulation from a file.
    """
    @classmethod
    def load(cls, path):
        sim = cls(0,0)
        # Load simulation from path
        with open(path, "r") as file:
            savestate = json.load(file)

        for floor_number in savestate["building"]:
            new_floor = Floor(int(floor_number), len(savestate["building"][floor_number]))
            for room_number in savestate["building"][floor_number]:
                room = Room(int(room_number), new_floor)
                room.has_zombies = savestate["building"][floor_number][room_number]["has_zombies"]
                room.blocked = savestate["building"][floor_number][room_number]["blocked"]
                room.sensor.state = State[savestate["building"][floor_number][room_number]["sensor_state"]]
            sim.building.floors.append(new_floor)
        
        sim.time = savestate["time"]
        return sim

    
    def save(self, path):
        savestate = {
            "building": {
                floor.number : {
                    room.number : {
                        "has_zombies": room.has_zombies,
                        "blocked": room.blocked,
                        "sensor_state": room.sensor.state.name
                    } 
                    for room in floor.rooms
                } 
                for floor in self.building.floors  
            },
            "time": self.time}
        # Save simulation to path
        with open(path, "w") as file:
            json.dump(savestate, file)
        

        

    def __init__(self, number_of_rooms, number_of_floors):
        self.building = Building(number_of_floors, number_of_rooms)
        self.time = 0
    
    def add_zombies(self, floor_number, room_number):
        self.building.floors[floor_number].rooms[room_number].has_zombies = True
    
    def block_room(self, floor_number, room_number):
        self.building.floors[floor_number].rooms[room_number].blocked = True
    

    def print_state(self):
        for sensor in Sensor.all:
            print(sensor)
    
    def update_sensors(self):
        for sensor in Sensor.all:
            sensor.update()
        
    def reset_sensor(self, floor_number, room_number):
        self.building.floors[floor_number].rooms[room_number].sensor.reset()

    def update(self):
        """
        Moves zombies to adjacent rooms and updates the simulation.
        """
        for floor in self.building.floors:

            for room in floor.rooms:

                if room.blocked or room.visited:
                    continue
                elif room.has_zombies:
                    # Expand zombies
                    for idx in range(4):
                        # (-1, 0), (1, 0), (0, -1), (0, 1)
                        i = idx % 2 * (idx - 2)
                        j = (idx + 1) % 2 * (idx - 1)

                        # verify index error
                        try:
                            new_room = self.building.floors[floor.number + i].rooms[room.number + j]
                        except IndexError:
                            continue

                        if new_room.visited or new_room.blocked:
                            continue
                        else:
                            new_room.has_zombies = True
                            new_room.visited = True
                        
                    # Decide wether or not zombies leave the room
                    if randint(0, 1) == 1:
                        room.has_zombies = False

                    room.visited = True
        
        # Unvisit all rooms
        for floor in self.building.floors:
            for room in floor.rooms:
                room.visited = False
        
        # update sensors
        self.update_sensors()
        
        # update time
        self.time += 1
        




