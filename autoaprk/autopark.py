"""
Task: Autopark
1. Create basic class Car with attributes: brand, model, year, color, mileage, is_working, rent_price (for 1 km), fix_price. Methods: drive(km), __str__()
2. Create classes ElectricCar and GasCar that inherit from Car.
3. Create class Autopark with attributes: name, cars (list of Car objects), total_profit. Methods: add_car(car), remove_car(car), rent_car(car, km), repair_car(car, price), __str__().
"""
import random

class Car:
    def __init__(self, brand , model , year , color , mileage , is_working , rent_price , fix_price):
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.is_working = is_working
        self.rent_price = rent_price
        self.fix_price = fix_price

    def drive(self, km):
        pass

    def random_fix_price(self):
        if random.randint(0, 10) == 0:
            return random.randint(500, 20000)
        return 0

    def __str__(self):
        return f'''brand = {self.brand} , model = {self.model} , year = {self.year}
                 color = {self.color} , mileage = {self.mileage}
                 is_working = {self.is_working}
                rent_price = {self.rent_price} , fix_price = {self.fix_price}'''





class ElectricCar(Car):

    def __init__(self, brand, model, year, color, mileage, is_working, rent_price, fix_price, break_system_price, battery_price, charging_cables_price):
        super().__init__(brand, model, year, color, mileage, is_working, rent_price, fix_price)

        self.break_system_price = break_system_price
        self.battery_price = battery_price
        self.charging_cables_price = charging_cables_price
    def drive(self, km):
        self.mileage += km
        if self.mileage % 40000 < km:
            self.fix_price += self.charging_cables_price
        elif self.mileage % 10000 < km:
            self.fix_price += self.break_system_price
        elif self.mileage % 150000 < km:
            self.fix_price += self.battery_price

        self.fix_price += self.random_fix_price()


class GasCar(Car):
    def __init__(self, brand, model, year, color, mileage, is_working, rent_price, fix_price, oil_price, break_system_price, engine_price):
        super().__init__(brand, model, year, color, mileage, is_working, rent_price, fix_price)
        self.oil_price = oil_price
        self.break_system_price = break_system_price
        self.engine_price = engine_price

    def drive(self, km):
        self.mileage += km
        if self.mileage % 40000 < km:
            self.fix_price += self.break_system_price
        elif self.mileage % 10000 < km:
            self.fix_price += self.oil_price
        elif self.mileage % 150000 < km:
            self.fix_price += self.engine_price

        self.fix_price += self.random_fix_price()




class Autopark:
    def __init__(self, name):
        self.name = name
        self.cars = []
        self.total_profit = 15000

    def add_car(self, car):
        self.cars.append(car)
        print(f"Car {car.brand} {car.model} added to the autopark.")

    def remove_car(self, car):
        if car in self.cars:
            self.cars.remove(car)
            print(f"Car {car.brand} {car.model} removed from the autopark.")
        else:
            print("Car not found in autopark.")
    def rent_car(self, car, km):
        if car in self.cars and car.is_working:
                car.drive(km)
                profit = km * car.rent_price
                self.total_profit += profit
        else:
                print(f"Cannot rent {car.model}. It may be not working or not in autopark.")

    def repair_car(self, car, price=None):
            if car in self.cars:
                fix_cost = price if price is not None else car.fix_price
                self.total_profit -= fix_cost
                car.is_working = True
                car.fix_price = 0
            else:
                print(f"{car.model} not found in autopark.")



# camel case - myVariable
# kebab case - my-variable
# snake case - my_variable
# classes in Python MyClass


toyota = GasCar (brand="toyota" , model="LandCruiser300", year="2021" , color="black",mileage=0,is_working=True,rent_price=250,fix_price=0,oil_price=200,break_system_price=1000,engine_price=5000)
bmwi4 = ElectricCar(brand="bmw" , model="i4", year="2021" , color="black",mileage=0,is_working=True,rent_price=2,fix_price=0,break_system_price=600,battery_price=10000,charging_cables_price=250)
park = Autopark("zrxson Autopark")
park.add_car(bmwi4)
park.add_car(toyota)

for i in range(10):
    park.rent_car(bmwi4,random.randint(200, 500))
    print(park.total_profit)

park.repair_car(bmwi4)
print(park.total_profit)
park.remove_car(bmwi4)
print(park)
park.rent_car(bmwi4,400)
print(park.total_profit)
