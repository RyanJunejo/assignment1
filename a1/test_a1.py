"""Assignment 1 - Grocery Store Simulation

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory are
Copyright (c) Jonathan Calver, Diane Horton, Sophia Huynh, Joonho Kim and
Jacqueline Smith.

Module Description:
This module contains some starter tests for Assignment 1.
You may add additional tests here, but you will not hand in this file.
"""
from io import StringIO
from simulation import GroceryStoreSimulation
from event import create_event_list
from store import GroceryStore, Customer, Item
from store import RegularLine, ExpressLine, SelfServeLine
from event import create_event_list
from simulation import GroceryStoreSimulation

CONFIG_FILE = '''{
  "regular_count": 1,
  "express_count": 0,
  "self_serve_count": 0,
  "line_capacity": 1
}
'''

EVENT_FILE = '''10 Arrive Tamara Bananas 7
5 Arrive Jugo Bread 3 Cheese 3
'''


# a provided sample test for the whole simulation
def test_simulation() -> None:
    """Test two events and single checkout simulation."""
    gss = GroceryStoreSimulation(StringIO(CONFIG_FILE))
    gss.run(create_event_list(StringIO(EVENT_FILE)))
    assert gss.stats == {'num_customers': 2, 'total_time': 18, 'max_wait': 8}


# Note: You can write additional tests here or in a separate file
# You will hand in this file. The only tests you will hand in are your tests
# for class PriorityQueue in file test_container.py.


CONFIG_FILE_2 = '''{
  "regular_count": 0,
  "express_count": 1,
  "self_serve_count": 0,
  "line_capacity": 1
}
'''


def test_simulation_express() -> None:
    gss = GroceryStoreSimulation(StringIO(CONFIG_FILE_2))
    gss.run(create_event_list(StringIO(EVENT_FILE)))
    assert gss.stats == {'num_customers': 2, 'total_time': 18, 'max_wait': 8}


CONFIG_FILE_3 = '''{
  "regular_count": 0,
  "express_count": 0,
  "self_serve_count": 1,
  "line_capacity": 1
}
'''


def test_simulation_self_serve() -> None:
    gss = GroceryStoreSimulation(StringIO(CONFIG_FILE_3))
    gss.run(create_event_list(StringIO(EVENT_FILE)))
    assert gss.stats == {'num_customers': 2, 'total_time': 31, 'max_wait': 21}


CONFIG_FILE_CLOSE = '''{
  "regular_count": 2,
  "express_count": 0,
  "self_serve_count": 0,
  "line_capacity": 1
}
'''

EVENT_FILE_CLOSE = '''10 Arrive Tamara Bananas 7
5 Arrive Jugo Bread 3 Cheese 3
0 Close 0
'''


def test_simulation_close() -> None:
    """Test two events and single checkout simulation."""
    gss = GroceryStoreSimulation(StringIO(CONFIG_FILE_CLOSE))
    gss.run(create_event_list(StringIO(EVENT_FILE_CLOSE)))
    assert gss.stats == {'num_customers': 2, 'total_time': 18, 'max_wait': 8}


if __name__ == '__main__':
    import pytest

    pytest.main(['test_a1.py'])

# RANDOM OTHER TEST NOT FROM TEST A1
store_config_list = [
    'input_files/config_001_10.json',
    'input_files/config_010_10.json',
    'input_files/config_100_01.json',
    'input_files/config_100_10.json',
    'input_files/config_111_01.json',
    'input_files/config_111_10.json',
    'input_files/config_300_01.json',
    'input_files/config_300_10.json',
    'input_files/config_333_01.json',
    'input_files/config_333_10.json',
    'input_files/config_642_05.json',
]

events_config_list = [
    'input_files/events_base.txt',
    'input_files/events_mixtures.txt',
    'input_files/events_no_express.txt',
    'input_files/events_one.txt',
    'input_files/events_one_at_a_time.txt',
    'input_files/events_one_close.txt',
    'input_files/events_two.txt',
]


def simulation_all_combinations() -> None:
    """Test two events and single checkout simulation."""

    for store_name in store_config_list:
        for events_name in events_config_list:
            close_line_error = False
            store_config = open(store_name)
            events_config = open(events_name)

            gss = GroceryStoreSimulation(store_config)
            gss.run(create_event_list(events_config))
            print(f'{events_name[12:]} in store_{store_name[12:]} = {gss.stats}')

            store_config.close()
            events_config.close()


if __name__ == '__main__':
    simulation_all_combinations()
