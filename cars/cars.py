class Transport():
	def __init__(self, name, color, max_speed, wheels):
		self.__name = name
		self.__color = color
		self.__max_speed = max_speed
		self.__wheels = wheels

	def get_name(self):
		return self.__name
	
	def get_color(self):
		return self.__color
	
	def get_max_speed(self):
		return self.__max_speed
	
	def get_wheels(self):
		return self.__wheels
	
	def set_name(self, name):
		self.__name = name
	
	def set_color(self, color):
		self.__color = color

	def set_max_speed(self, max_speed):
		self.__max_speed = max_speed

	def set_wheels(self, wheels):
		self.__wheels = wheels

	def move(self):
		return f"{self.__name} is moving at {self.__max_speed} km/h."

	def __str__(self):
		return f"Transport: \nname={self.__name}, \ncolor={self.__color}, \nmax_speed={self.__max_speed}, \nwheels={self.__wheels}\n"
	
class EngineTransport(Transport):
	def __init__(self, name, color, max_speed, wheels, engine, transmission, fuel_tank):
		super().__init__(name, color, max_speed, wheels)
		self.__engine = engine
		self.__transmission = transmission
		self.__fuel_tank = fuel_tank
		self.__is_started = False

	def get_engine(self):
		return self.__engine
	
	def get_transmission(self):
		return self.__transmission
	
	def get_fuel_tank(self):
		return self.__fuel_tank
	
	def set_engine(self, engine):
		self.__engine = engine

	def set_transmission(self, transmission):
		self.__transmission = transmission

	def set_fuel_tank(self, fuel_tank):
		self.__fuel_tank = fuel_tank

	def is_started(self):
		return self.__is_started
	
	def set_started(self, is_started):
		self.__is_started = is_started

	def start_engine(self):
		if not self.__is_started:
			self.__is_started = True
			return f"{self.__engine} engine started."
		else:
			return "Engine is already started."

	def move(self):
		if self.__is_started:
			return super().move()
		else:
			return "Start the engine first before moving."

	def __str__(self):
		return super().__str__() + f"engine={self.__engine}, \ntransmission={self.__transmission}, \nfuel_tank={self.__fuel_tank}\n"
	
class Truck(EngineTransport):
	def __init__(self, name, color, max_speed, wheels, engine, transmission, fuel_tank, max_load, current_load):
		super().__init__(name, color, max_speed, wheels, engine, transmission, fuel_tank)
		self.__max_load = max_load
		self.__current_load = current_load

	def move(self):
		if self.is_started() and self.__current_load <= self.__max_load:
			return super().move()
		else:
			return "Cannot move: either the engine is not started or the load exceeds the maximum load."

	def __str__(self):
		return super().__str__() + f"max load={self.__max_load}\n current load={self.__current_load}\n"
	
class Part():
	def __init__(self, name):
		self.__name = name

	def get_name(self):
		return self.__name
	
	def set_name(self, name):
		self.__name = name

	def __str__(self):
		return f"Part: \nname={self.__name}\n"
	
class Engine(Part):
	def __init__(self, name, power):
		super().__init__(name)
		self.__power = power

	def get_power(self):
		return self.__power
	
	def set_power(self, power):
		self.__power = power

	def __str__(self):
		return super().__str__() + f"power={self.__power}\n"
	
class Transmission(Part):
	def __init__(self, name, type):
		super().__init__(name)
		self.__type = type

	def get_type(self):
		return self.__type
	
	def set_type(self, type):
		self.__type = type

	def __str__(self):
		return super().__str__() + f"type={self.__type}\n"
	
class FuelTank(Part):
	def __init__(self, name, capacity):
		super().__init__(name)
		self.__capacity = capacity

	def get_capacity(self):
		return self.__capacity
	
	def set_capacity(self, capacity):
		self.__capacity = capacity

	def __str__(self):
		return super().__str__() + f"capacity={self.__capacity}\n"
	
class Wheel(Part):
	def __init__(self, name, diameter):
		super().__init__(name)
		self.__diameter = diameter

	def get_diameter(self):
		return self.__diameter
	
	def set_diameter(self, diameter):
		self.__diameter = diameter

	def __str__(self):
		return super().__str__() + f"diameter={self.__diameter}\n"
class Car(EngineTransport):
	def __init__(self, name, color, max_speed, wheels, engine, transmission, fuel_tank):
		super().__init__(name, color , max_speed , wheels , engine , transmission , fuel_tank)


	def move(self):
		if self.is_started():
			return super().move()

engine_s63 = Engine("BMW S63", 625)
transmission_8hp = Transmission("ZF 8HP", "automatic")
fuel_tank_68 = FuelTank("BMW M5 Tank", 68)
wheel_20 = Wheel("Pirelli P Zero", 20)
bmw_m5_f90 = Car("BMW M5 F90", "grey", 305, wheel_20, engine_s63, transmission_8hp, fuel_tank_68)
print(bmw_m5_f90)
print(bmw_m5_f90.start_engine())
print(bmw_m5_f90.move())


class Bike(Transport):
	def __init__(self,name , color , max_speed , wheels, bike_type):
		super().__init__(name , color , max_speed , wheels ,)
		self._bike_type = bike_type
	def move(self):
		if self._bike_type == "mountain_bike":
			return f"{self._bike_type} {self.get_name()} is moving in the mountains with the {self.get_max_speed()} km/h"
		elif self._bike_type == "town_bike":
			return f"{self._bike_type} {self.get_name()} is moving in the city with the  {self.get_max_speed()} km/h"
		elif self._bike_type == "road_bike":
			return f"{self._bike_type} {self.get_name()} is moving on the road with the  {self.get_max_speed()} km/h"
mountain_bike = Bike("Giant Talon", "green", 35, 29, "mountain_bike")
town_bike = Bike("Gazelle CityGo", "blue", 25, 28, "town_bike")
road_bike = Bike("Trek Domane", "red", 45, 28, "road_bike")
#
# print(mountain_bike)
# print(mountain_bike.move())
#
# print(town_bike)
# print(town_bike.move())
#
# print(road_bike)
# print(road_bike.move())


# mishelin_70 = Wheel("Mishelin", 70)
# om_471 = Engine("Mersedes OM 471", 625)
# g_330 = Transmission("Mersedes G330", "automatic")
# tank_500 = FuelTank("Mersedes fuel tank", 500)
# mersedes_actros = Truck("Mersedes Actros", "red", 150, mishelin_70, om_471, g_330, tank_500, 20000, 25000)
# print(mersedes_actros)
# print(mersedes_actros.start_engine())
# print(mersedes_actros.move())
#
# mersedes_arocs = Truck("Mersedes Arocs", "blue", 140, mishelin_70, om_471, g_330, tank_500, 18000, 15000)
# print(mersedes_arocs)
# print(mersedes_arocs.start_engine())
# print(mersedes_arocs.move())