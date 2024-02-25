"""Assignment 1 - Grocery Store Models (Task 1)

CSC148 Winter 2024
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory are
Copyright (c) Jonathan Calver, Diane Horton, Sophia Huynh, Joonho Kim and
Jacqueline Smith.

Module Description:

This file contains all the classes necessary to model the relevant entities
in a grocery store.
"""
from __future__ import annotations
from typing import TextIO
import json

# The maximum number of items a customer can have if they use an express line.
EXPRESS_LIMIT = 7


class NoAvailableLineError(Exception):
    """Represents a situation in which a customer has arrived at the checkout
    area and there is no line available for them to join.
    """

    def __str__(self) -> str:
        return 'No line available'


class GroceryStore:
    """A grocery store.

    A grocery store consists of checkout lines.

    TODO: Add one or more attributes to store the checkout lines.
        Include documentation, a type contract, and appropriate Representation
        Invariants for any attribute(s) you add.

    Attributes:
    - num_lines: How many lines this grocery store has.
    - line_capacity: How many people can queue in a line
    - regular_count: index where regular line starts
    - express_count: index where express line starts
    - self_serve_count: index where self serve line starts
    - self.lines: list of lines

    Representation Invariants:
    - self.num_lines > 0
    - self.line_capacity > 0
    -self.regular_count >= 0
    - self.express_count >= 0
    - self.self_serve_count >= 0

    """
    num_lines: int
    line_capacity: int
    regular_count: int
    express_count: int
    self_serve_count: int
    lines : list

    def __init__(self, config_file: TextIO) -> None:
        """Initialize a GroceryStore from a configuration file <config_file>.

        Preconditions:
        - config_file is a valid JSON configuration file with the keys
          regular_count, express_count, self_serve_count, and line_capacity
        - config_file is open
        - All values in config_file are >= 0
        """
        config = json.load(config_file)
        self.line_capacity = config('line_capacity')
        self.regular_count = config('regular_count')
        self.express_count = config('express_count')
        self.self_serve_count = config('self_serve_count')
        self.num_lines = self.regular_count + self.express_count + self.self_serve_count
        self.lines = []

        for i in range(self.regular_count):
            self.lines.append(RegularLine(self.line_capacity))

        # Create ExpressLine instances
        for i in range(self.express_count):
            self.lines.append(ExpressLine(self.line_capacity))

        # Create SelfServeLine instances
        for i in range(self.self_serve_count):
            self.lines.append(SelfServeLine(self.line_capacity))

    def enter_line(self, customer: Customer) -> int:
        """Pick a new line for <customer> to join, using the algorithm from
        the handout and add <customer> to that line.

        Return the index of the line that the customer joined.

        Raise a NoAvailableLineError if there is no line available for the
        customer to join.

        Preconditions:
        - customer is not currently in any line in this GroceryStore
        """
        a, b = [], []
        if customer.num_items < 8:
            for line in self.lines:
                a.append(len(line))  # Number of people in line is the length of the list of customers
            if a:
                min_length = min(a)
                chosen_line_index = a.index(min_length)
                self.lines[chosen_line_index].append(customer)
                return chosen_line_index

        elif customer.num_items >= 8:
            for line in self.lines:
                if not isinstance(line, ExpressLine):
                    b.append(line)
            if b:
                for line in b:
                    a.append(len(line))  # Number of people in line is the length of the list of customers
                if a:
                    min_length = min(a)
                    chosen_line_index = a.index(min_length)
                    self.lines[chosen_line_index].append(customer) #change this to accept probably or try it
                    return chosen_line_index

        raise NoAvailableLineError()



    def next_checkout_time(self, line_number: int) -> int:
        """Return the time it will take to check out the customer at the front
        of line <line_number>.

        Preconditions:
        - 0 <= line_number < self.num_lines
        """
        line = self.lines[line_number]
        if line.is_empty(): #change these
            raise NoAvailableLineError("No customer is in the line")
        customer = line.first_in_line()
        return customer.item_time()


    def remove_front_customer(self, line_number: int) -> int:
        """If there is any customer (or customers) in checkout line
        <line_number>, remove the front customer.

        Return the number of customers remaining in line <line_number>.

        Preconditions:
        - 0 <= line_number < self.num_lines
        """
        line = self.lines[line_number]
        if line.is_empty():
            raise NoAvailableLineError("No customer is in the line")
        line.pop(0)
        return len(line)


    def close_line(self, line_number: int) -> list[Customer]:
        """Close checkout line <line_number> by updating its status to indicate
        that it is closed and removing from it all customers after the first
        one.

        Return a new list with these removed customers, in the same order as
        they appeared in the line before it closed.

        Preconditions:
        - 0 <= line_number < self.num_lines
        """
        line = self.lines[line_number]

        # Check if the line is already closed
        if line.is_closed:
            raise ValueError("Line is already closed")

        # Get all customers after the first one
        removed_customers = line[1:]

        # Update the line status to closed
        line.close()

        # Remove all customers after the first one from the line
        del line[1:]

        return removed_customers

    def first_in_line(self, line_number: int) -> Customer | None:
        """Return the first customer in line <line_number>, or None if there
        are no customers in line.

        Do not change the line, however.

        Preconditions:
        - 0 <= line_number < self.num_lines
        """
        line = self.lines[line_number]
        if line:
            return line[0]
        else:
            return None


class Customer:
    """A grocery store customer.

    Attributes:
    - name: A unique identifier for this customer.
    - arrival_time: The first time this customer arrived at the checkout area
      and attempted to join a line, or None if they have not yet arrived.
    - _items: The items this customer has.

    Representation Invariants:
    - self.arrival_time is None or self.arrival_time >= 0
    """
    name: str
    arrival_time: int | None
    _items: list[Item]

    def __init__(self, name: str, items: list[Item]) -> None:
        """Initialize a customer with the given <name> and a copy of the
        list <items>.

        The customer's arrival_time is initially None.

        >>> item_list = [Item('bananas', 7)]
        >>> belinda = Customer('Belinda', item_list)
        >>> belinda.name
        'Belinda'
        >>> belinda._items == item_list
        True
        >>> belinda._items is item_list
        False
        >>> belinda.arrival_time is None
        True
        """
        self.name = name
        self._items = items
        self.arrival_time = None

    def num_items(self) -> int:
        """Return the number of items this customer has.

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.num_items()
        2
        """
        return len(self._items)

    def item_time(self) -> int:
        """Return the number of seconds it takes for a cashier to check out
        this customer, that is, the time it takes to check out this customer
        at a regular or express line.

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.item_time()
        10
        """
        a = 0
        for i in self._items:
            a += i.time
        return a



class Item:
    """An item to be checked out.

    Attributes:
    - name: the name of this item
    - time: the amount of time it takes a cashier to check out this item

    Representation Invariants:
    - self.time > 0
    """
    name: str
    time: int

    def __init__(self, name: str, time: int) -> None:
        """Initialize a new item with <name> and <time>.

        Preconditions:
        - time > 0

        >>> item = Item('bananas', 7)
        >>> item.name
        'bananas'
        >>> item.time
        7
        """
        self.name = name
        self.time = time


class CheckoutLine:
    """A checkout line in a grocery store.

    This is an abstract class and should not be instantiated.

    Attributes:
    - capacity: The maximum number of customers allowed in this CheckoutLine.
    - is_open: True iff the line is open.
    - _queue: Customers in this line in order by arrival time, with the
                earliest arrival at the front of the list.

    Representation Invariants:
    - len(self) <= self.capacity
    - capacity > 0
    """
    capacity: int
    is_open: bool
    _queue: list[Customer]

    def __init__(self, capacity: int) -> None:
        """Initialize an open and empty CheckoutLine, with the given <capacity>.

        Preconditions:
        - capacity > 0

        >>> line = CheckoutLine(1)
        >>> line.capacity
        1
        >>> line.is_open
        True
        >>> line._queue
        []
        """
        self.capacity = capacity
        self.is_open = True
        self._queue = []

    def __len__(self) -> int:
        """Return the length of this CheckoutLine.

        >>> line = CheckoutLine(10)
        >>> len(line)
        0
        """
        return len(self._queue)

    def can_accept(self, customer: Customer) -> bool:
        """Return True iff this CheckoutLine can accept <customer>.

        >>> line = CheckoutLine(1)
        >>> line.can_accept(Customer('Sophia', []))
        True
        """
        if len(line) < self.capacity:
            return True
        else:
            return False



    def accept(self, customer: Customer) -> bool:
        """Accept <customer> into the end of this CheckoutLine if possible.

        Return True iff the customer is accepted.

        >>> line = CheckoutLine(1)
        >>> c1 = Customer('Belinda', [Item('cheese', 3)])
        >>> c2 = Customer('Hamman', [Item('chips', 4), Item('gum', 1)])
        >>> line.accept(c1)
        True
        >>> line.accept(c2)
        False
        >>> len(line)
        1
        >>> line.first_in_line() is c1
        True
        """
        if self.can_accept(customer)
            self._queue.append(customer)
            return True
        else
            return False


    def next_checkout_time(self) -> int:
        """Return the time it will take to check out the customer at the front
        of this line.

        Preconditions:
        - self.first_in_line() is not None

        No doctests provided, since this method is abstract.
        """
        raise NotImplementedError

    def remove_front_customer(self) -> int:
        """If there is any customer (or customers) in this checkout line,
        remove the front customer.

        Return the number of customers remaining in the line.

        >>> line = CheckoutLine(1)
        >>> line.accept(Customer('Sophia', [Item('red snapper', 21)]))
        True
        >>> line.remove_front_customer() # No one is left in line.
        0
        >>> line.remove_front_customer() # It's still okay to call the method.
        0
        """
        if len(self._queue) == 0:
            return 0
        else:
            v = self._queue.pop[0]
            return len(self._queue)




    def close(self) -> list[Customer]:
        """Close this line by updating its status to indicate that it is closed
        and removing from it all customers after the first one.

        Return a new list with these removed customers, in the same order as
        they appeared in the line before it closed.

        >>> line = CheckoutLine(2)
        >>> line.close()
        []
        >>> line.is_open
        False
        """
        self.is_open = False
        a = self._queue[1:]
        self._queue = [self._queue[0]]
        return a

    def first_in_line(self) -> Customer | None:
        """Return the first customer in this line, or None if there are no
        customers in line.

        Do not change the line, however.

        >>> line = CheckoutLine(1)
        >>> line.first_in_line() is None
        True
        """
        if len(self._queue) == 0
            return None
        else:
            return self._queue[0]



# TODO: create subclasses for the different types of events below.
class RegularLine(CheckoutLine):
    """A regular CheckoutLine.
    """
    # TODO: Implement this class


class ExpressLine(CheckoutLine):
    """An express CheckoutLine.
    """
    # TODO: Implement this class


class SelfServeLine(CheckoutLine):
    """A self-serve CheckoutLine.
    """
    # TODO: Implement this class


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    check_pyta = True
    if check_pyta:
        import python_ta

        python_ta.check_all(config={
            'allowed-import-modules': ['__future__', 'typing', 'json',
                                       'python_ta', 'doctest'],
            'disable': ['W0613']})
