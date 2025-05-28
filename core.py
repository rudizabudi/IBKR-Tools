from collections import defaultdict
from enum import StrEnum
from datetime import datetime
import json
import os
import threading
from typing import Any, Callable

from ibapi.contract import Contract as ibContract
from gui.tabs.tabs import Tabs

#from services.contracts import Position

type ContractInstance = 'ContractInstance'
type SubPageInstance = 'SubPageInstance'
type QtObj = 'QtObj'
type QTFunc = 'QTFunc'

type _T = 'T'


class Core:
    def __init__(self):
        self.load_config()
        self.create_var_space()

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

    @classmethod
    def create_var_space(cls):
        #TODO: Move as much as possible away from globalish space
        from services.backend import Backend
        cls.backend = Backend(cls)

        cls.threading_events: defaultdict[str, threading.Event] = defaultdict()

        cls.update_intervals: dict[str, int] = {'beta_weighted_deltas': 60}  # in secs

        cls.account_list: list[str] = []

        cls.active_tab: Tabs = Tabs.HOME

        cls.raw_positions: dict[str, dict[str, any]] = {}

        cls.positions: list[ContractInstance] = []
        cls.positions_str_sorted: list[str] = []

        cls.pos_betas: dict[str, float] = {}

        cls.table_contents: dict[str, list[str | float]] = {}

        cls.item_register: dict[str, QtObj] = {}
        cls.underlying_prices: dict[str, float] = {}

        cls.bwd_update_refresh: QTFunc = None

        cls.bxs_index_contract: dict[str, ibContract] = {}

        cls.widget_registry: dict[str, dict[str, QtObj]] = {}

        cls.tab_instances: dict[str, 'SubClassInstance'] = {}
        #TODO: Global event trigger class to handle services <-> gui interactions
        cls.project_font = None


class CoreDistributor:
    #TODO: Make a wrapper out of this
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


class ReqId:
    _lock = threading.Lock()
    reqId_hashmap: defaultdict = defaultdict()
    _reqId = 0

    @classmethod
    def register_reqId(cls, target: Callable = None):
        with cls._lock:
            cls._reqId += 1
            cls.reqId_hashmap[cls._reqId] = target
            return cls._reqId


def tprint(text: str = '', *args, **kwargs):
    print(f'{datetime.now().strftime('%H:%M:%S')} : {text}')


class RequestState(StrEnum):
    REQUESTED = 'Requested'
    RECEIVED = 'Received'
