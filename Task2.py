import json
import os
import dataclasses
from datetime import datetime


class Kitchen:
    """Class for getting info on ingredients quantity, storing it and handling order creation"""
    def __init__(self, stock_info):
        if not os.path.isfile(stock_info):
            raise ValueError("Kitchen stock info doesnt exist")
        self.file_name = stock_info
        with open(stock_info, "r") as inp:
            self.stock_info = json.load(inp)

    def __del__(self):
        """Update info on used products"""
        with open(self.file_name, "w") as upd:
            json.dump(self.stock_info, upd, indent=4)

    def available_addons(self, customer):
        """Getting info on available addons based on day of the week and ingredients availability"""
        addons = []
        base_required = dataclasses.asdict(self.get_order(customer, True))
        for keys in self.stock_info.keys():
            if self.stock_info[keys] > 1:
                if self.stock_info[keys] - base_required[keys] > 0:
                    addons.append((keys, self.stock_info[keys]))
        return addons

    def get_order(self, customer, *check, **kwargs):
        """Create an order and subtract used up ingredients"""
        if not isinstance(customer, Customer):
            raise TypeError("Client should be customer type")
        price = 100
        if kwargs:
            price += len(kwargs)*5
        match customer.date.weekday():
            case 0:
                obj = Mondaypizza(price, **kwargs)
            case 1:
                obj = Tuesdaypizza(price, **kwargs)
            case 2:
                obj = Wednesdaypizza(price, **kwargs)
            case 3:
                obj = Thursdaypizza(price, **kwargs)
            case 4:
                obj = Fridaypizza(price, **kwargs)
            case _:
                obj = Weekendpizza(price, **kwargs)
        required = dataclasses.asdict(obj)
        if not check:
            for keys in required.keys():
                if keys == 'price':
                    continue
                self.stock_info[keys] -= required[keys]
                if self.stock_info[keys] < 0:
                    raise ValueError("Required products not in stock")
        return obj


@dataclasses.dataclass(frozen=True)
class Customer:
    """Class for storing info about a client"""
    name: str
    date: datetime


@dataclasses.dataclass(frozen=True)
class Pizzabase:
    """Base class storing info about pizza"""
    price: int
    sauce: int = 1
    cheese: int = 1
    beef: int = 0
    bbq_sauce: int = 0
    pepperoni: int = 0
    pepper: int = 0
    blue_cheese: int = 0
    ham: int = 0
    mushrooms: int = 0
    feta_cheese: int = 0
    cheddar_cheese: int = 0
    pork: int = 0
    sausage: int = 0
    bacon: int = 0

    def __str__(self):
        dictionary = dataclasses.asdict(self)
        return '  '.join([key+' '+str(dictionary[key]) for key in dictionary.keys() if dictionary[key]])


@dataclasses.dataclass(frozen=True, kw_only=True)
class Mondaypizza(Pizzabase):
    pepperoni: int = 1
    pepper: int = 1


@dataclasses.dataclass(frozen=True, kw_only=True)
class Tuesdaypizza(Pizzabase):
    pepperoni: int = 1
    blue_cheese: int = 1


@dataclasses.dataclass(frozen=True, kw_only=True)
class Wednesdaypizza(Pizzabase):
    beef: int = 1
    bbq_sauce: int = 1


@dataclasses.dataclass(frozen=True, kw_only=True)
class Thursdaypizza(Pizzabase):
    ham: int = 1
    mushrooms: int = 1


@dataclasses.dataclass(frozen=True, kw_only=True)
class Fridaypizza(Pizzabase):
    blue_cheese: int = 1
    feta_cheese: int = 1
    cheddar_cheese: int = 1


@dataclasses.dataclass(frozen=True, kw_only=True)
class Weekendpizza(Pizzabase):
    beef: int = 1
    pork: int = 1
    sausage: int = 1
    bacon: int = 1


def main():
    file = "kitchen.json"
    rest = Kitchen(file)
    maks = Customer("Maksim", datetime.now())
    print(rest.available_addons(maks))
    order = rest.get_order(maks, ham=1, pork=1)
    print(order)


if __name__ == '__main__':
    main()
