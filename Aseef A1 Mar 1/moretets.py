from io import StringIO
from simulation import GroceryStoreSimulation
from event import create_event_list
from store import GroceryStore, Customer, Item
from store import RegularLine, ExpressLine, SelfServeLine
from event import create_event_list
from simulation import GroceryStoreSimulation

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
