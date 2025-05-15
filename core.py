from dataclasses import dataclass
from datetime import datetime
import json
import os
import threading

#from services.contracts import Position

type ContractInstance = 'ContractInstance'
type SubPageInstance = 'SubPageInstance'
type DataHandlerInstance = 'DataHandlerInstance'
type QtObj = 'QtObj'
type QTFunc = 'QTFunc'


class Core:
    def __init__(self):
        pass

    @classmethod
    def load_config(cls):
        if os.getenv('DEV_VAR') == 'rudizabudi':
            config_file = 'config_dev.json'
        else:
            config_file = 'config.json'

        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'config.json')):
            raise FileNotFoundError(f"Config file '{config_file}' not found.")

        with open(os.path.join(os.path.dirname(__file__), config_file), 'r') as file:
            config = json.load(file)

        if len(config['profiles']) == 0:
            raise ValueError("No profiles found in the config file.")

        for i, x in enumerate(config['profiles'].keys(), start=1):
            print(f'Profile {i}: {x}')

        if len(config['profiles']) > 1:
            selection = -1
            while selection not in range(len(config['profiles'])):
                try:
                    selection = int(input('Select profile: ')) - 1
                except ValueError:
                    print('Invalid input. Please enter a number.')

            config = config['profiles'][list(config['profiles'].keys())[selection]]
        else:
            config = config['profiles'][list(config['profiles'].keys())[0]]

        try:
            cls.HOST_IP = config['api_host_ip']
            cls.API_PORT = config['api_port']
            cls.CLIENT_ID = config['api_client_id']
            cls.ACCOUNT_ID = config['ibkr_account_id']
            cls.BENCHMARK = config['beta_benchmark']
            cls.BETA_PERIOD = config['beta_period']

        except KeyError as e:
            raise KeyError(f'Missing key in config file: {e}')

    controller_loop_interval: int = 60  # in secs
    reqId_hashmap: dict = {}
    reqId: int = 1

    account_list: list[str] = []

    active_tab: str = ''

    raw_positions: dict[str, dict[str, any]] = {}

    requesting_positions: bool = False
    positions: list[ContractInstance] = []
    positions_str_sorted: list[str] = []

    pos_betas: dict[str: float] = {}

    table_contents: dict[str: list[str | float]] = {}

    item_register: dict[str: QtObj] = {}
    underlying_prices: dict[str: float] = {}

    bwd_update_refresh: QTFunc = None

    widget_registry: dict[str: dict[str: QtObj]] = {}
    tab_instances: dict[str: dict[str: DataHandlerInstance] | DataHandlerInstance] = {}
    #TODO: Global event trigger class to handle services <-> gui interactions
    project_font = None


@dataclass
class CoreDistributor:
    _lock = threading.Lock()
    _core_instance = None

    # Make core variable space threadsafe
    @classmethod
    def get_core(cls):
        if cls._core_instance is None:
            with cls._lock:
                if cls._core_instance is None:
                    cls._core_instance = Core()
        return cls._core_instance


def tprint(text: str = '', *args, **kwargs):
    print(f'{datetime.now().strftime('%H:%M:%S')} : {text}')
