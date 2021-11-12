import dataclasses
import json
import os
from datetime import datetime, timedelta

STUDENT_COEF = 0.5
ADVANCED_COEF = 0.6
LATE_COEF = 1.1
# Constants for calculating price of different types of tickets


class Event:
    """Class for getting info about event from json, storing it and creating tickets"""

    def __init__(self, event_info, tickets_storage):
        """Getting info about event from json file and getting tickets that might already exist"""
        if not os.path.isfile(event_info):
            raise ValueError("Event info doesnt exist!")
        if not os.path.isfile(tickets_storage):
            raise ValueError("Tickets storage doesnt exist!")
        self.event_info_file = event_info
        self.tickets_storage = tickets_storage
        with open(self.event_info_file, "r") as inp:
            event_data = json.load(inp)
        if os.stat(tickets_storage).st_size:
            with open(self.tickets_storage, "r") as log:
                self.__data = json.load(log)
        else:
            self.__data = []
        self.__name = event_data["event_name"]
        self.__event_date = datetime(event_data["year"], event_data["month"], event_data["day"], event_data["hour"])
        self.__tickets_left = event_data["max_tickets"]
        self.__base_price = event_data["price"]

    @property
    def name(self):
        return self.__name

    @property
    def event_date(self):
        return self.__event_date

    @property
    def tickets_left(self):
        return self.__tickets_left

    def __del__(self):
        """Update info on sold tickets and tickets, that remain"""
        with open(self.event_info_file, "r") as inp:
            info = json.load(inp)
        info["max_tickets"] = self.__tickets_left
        with open(self.event_info_file, "w") as out:
            json.dump(info, out, indent=4)
        with open(self.tickets_storage, "w") as log:
            json.dump(self.__data, log, indent=4)

    def __str__(self):
        return f'Event: {self.name}, happens on {self.event_date}, tickets left: {self.__tickets_left}, ' \
               f'base price: {self.__base_price} '

    def get_ticket(self, customer):
        """Creating a ticket based on customer that wants to buy it"""
        if not isinstance(customer, Customer):
            raise TypeError("Buyer should be customer type!")
        if not self.__tickets_left:
            print("No tickets left")
            return None
        if customer.is_student:
            res = StudentTicket(self.name, customer.name, self.__base_price, len(self.__data)+1)
        elif self.event_date - customer.date > timedelta(60):
            res = AdvanceTicket(self.name, customer.name, self.__base_price, len(self.__data)+1)
        elif self.event_date - customer.date < timedelta(10):
            res = LateTicket(self.name, customer.name, self.__base_price, len(self.__data)+1)
        else:
            res = Ticket(self.name, customer.name, self.__base_price, len(self.__data)+1)
        self.__data.append(dataclasses.asdict(res))
        self.__tickets_left -= 1
        return res

    def get_price(self, customer):
        """Return a price of ticket for event based on customer, who asks"""
        if not isinstance(customer, Customer):
            raise TypeError("Buyer should be customer type!")
        price = self.__base_price
        if customer.is_student:
            return round(price * STUDENT_COEF, 2)
        elif self.event_date - customer.date > timedelta(60):
            return round(price * ADVANCED_COEF, 2)
        elif self.event_date - customer.date < timedelta(10):
            return round(price * LATE_COEF, 2)
        else:
            return price

    def search_by_id(self, inp_id):
        """Get a ticket by its id, returns None if not found"""
        for vals in self.__data:
            if vals["ticket_id"] == inp_id:
                return vals
        return None


@dataclasses.dataclass(frozen=True)
class Customer:
    """A class for storing info about a client(name, if he is a student and date of his request)"""
    name: str
    is_student: bool
    date: datetime


@dataclasses.dataclass(frozen=True)
class Ticket:
    """Class for storing info about a ticket"""
    event: str
    client_name: str
    price: float
    ticket_id: int


@dataclasses.dataclass(frozen=True)
class AdvanceTicket(Ticket):
    """A subclass for tickets bought in 60 or more days advance"""

    def __post_init__(self):
        object.__setattr__(self, "price", round(self.price * ADVANCED_COEF, 2))


@dataclasses.dataclass(frozen=True)
class StudentTicket(Ticket):
    """A subclass for tickets bought by students"""

    def __post_init__(self):
        object.__setattr__(self, "price", round(self.price * STUDENT_COEF, 2))


@dataclasses.dataclass(frozen=True)
class LateTicket(Ticket):
    """A subclass for tickets bought 10 days or later before the event"""

    def __post_init__(self):
        object.__setattr__(self, "price", round(self.price * LATE_COEF, 2))


def main():
    event_info = "event_info.json"
    ticket_storage = "tickets.json"
    concert = Event(event_info, ticket_storage)
    john = Customer("John", False, datetime(2021, 4, 18))
    mark = Customer("Mark", True, datetime(2021, 5, 1))
    print(concert.get_price(john))
    ticket = concert.get_ticket(john)
    ticket2 = concert.get_ticket(mark)
    print(ticket)
    print(concert.search_by_id(3))


if __name__ == '__main__':
    main()
