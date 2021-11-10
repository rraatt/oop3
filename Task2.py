import json
import os
import dataclasses
from datetime import datetime


class Kitchen:
    def __init__(self, stock_info):
        if not os.path.isfile(stock_info):
            raise ValueError("Kitchen stock info doesnt exist")
        with open(stock_info, "r") as inp:
            self.stock_info = json.load(inp)

    def get_order(self, customer):
        if not isinstance(customer, Customer):
            raise TypeError("Client should be customer type")
        match customer.date.weekday():
            case 0:
                obj = Mondaypizza()
            case 1:
                obj = Tuesdaypizza()
            case 2:
                obj = Wednesdaypizza()
            case 3:
                obj = Thursdaypizza()
            case 4:
                obj = Fridaypizza()
            case _:
                obj = Weekendpizza()
        required = dataclasses.asdict(obj)
        for keys in required.keys():
            self.stock_info[keys] -= required[keys]


@dataclasses.dataclass(frozen=True)
class Customer:
    name: str
    date: datetime


@dataclasses.dataclass(frozen=True)
class Pizzabase:
    dough = 1
    sauce = 1
    cheese = 1


@dataclasses.dataclass(frozen=True)
class Mondaypizza(Pizzabase):
    pepperoni = 1
    pepper = 1


@dataclasses.dataclass(frozen=True)
class Tuesdaypizza(Pizzabase):
    pepperoni = 1
    blue_cheese = 1


@dataclasses.dataclass(frozen=True)
class Wednesdaypizza(Pizzabase):
    beef = 1
    bbq_sauce = 1


@dataclasses.dataclass(frozen=True)
class Thursdaypizza(Pizzabase):
    ham = 1
    mushrooms = 1


@dataclasses.dataclass(frozen=True)
class Fridaypizza(Pizzabase):
    blue_cheese = 1
    feta_cheese = 1
    cheddar_cheese = 1


@dataclasses.dataclass(frozen=True)
class Weekendpizza(Pizzabase):
    beef = 1
    pork = 1
    sausage = 1
    bacon = 1
