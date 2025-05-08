import os
import threading
from dataclasses import dataclass
from datetime import datetime

from dotenv import load_dotenv

#from services.contracts import Position

type ContractInstance = 'ContractInstance'
type SubPageInstance = 'SubPageInstance'
type DataHandlerInstance = 'DataHandlerInstance'
type QtObj = 'QtObj'
type QTFunc = 'QTFunc'
load_dotenv('.env_dev_live')

if os.getenv('DEV_VAR') == 'rudizabudi':
    load_dotenv('.env_dev_live')
else:
    load_dotenv('.env')


class Core:
    def __init__(self, thread_id):
        self.thread_id = thread_id

    host_ip: str = os.getenv('HOST_IP')
    api_port: int = int(os.getenv('API_PORT'))

    client_id: int = int(os.getenv('CLIENT_ID'))
    account_id: str | None = os.getenv('ACCOUNT_ID') # TODO: Add selection popup if no account_Id provided

    benchmark: str = os.getenv('BENCHMARK')
    beta_period: str = os.getenv('BETA_PERIOD')

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

    project_font = None

    @classmethod
    def set_TWSCon(cls, TWSCon):
        cls.TWSCon = TWSCon

@dataclass
class CoreDistributor:
    _local = threading.local()

    @classmethod
    def get_core(cls):
        current_thread_id = threading.get_ident()

        if not hasattr(cls._local, 'core_instance'):
            cls._local.core_instance = Core(current_thread_id)
        return cls._local.core_instance


def tprint(text: str = '', *args, **kwargs):
    print(f'{datetime.now().strftime('%H:%M:%S')} : {text}')
