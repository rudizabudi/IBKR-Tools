from datetime import datetime, timedelta
from typing import TypeVar

from PyQt5.QtCore import pyqtSignal
from dotenv import load_dotenv
import os

load_dotenv('.env')

type ContractInstance = 'ContractInstance'
type SubPageInstance = 'SubPageInstance'
type QtObj = 'QtObj'
type QTFunc = 'QTFunc'


class Core:
    def __init__(self):
        self.host_ip: str = os.getenv('HOST_IP')
        self.api_port: int = int(os.getenv('API_PORT'))
        self.client_id: int = int(os.getenv('CLIENT_ID'))
        self.account_id: str | None = os.getenv('ACCOUNT_ID') # TODO: Add selection popup if no account_Id provided
        self.benchmark: str = os.getenv('BENCHMARK')
        self.beta_period: str = os.getenv('BETA_PERIOD')

        self.reqId_hashmap: dict = {}
        self.reqId: int = 1

        self.account_list: list[str] = []

        self.frame_tabs: dict[str: SubPageInstance] = {}
        self.active_tab: str = ''

        self.raw_positions: dict[str, dict[str: any]] = {}

        self.positions: list[ContractInstance] = []
        self.positions_str_sorted: list[str] = []

        self.table_contents: dict[str: list[str | float]] = {}

        self.item_register: dict[str: QtObj] = {}
        self.underlying_prices: dict[str: float] = {}

        self.bwd_update_refresh: QTFunc = None

    def set_TWSCon(self, TWSCon):
        self.TWSCon = TWSCon


def tprint(text: str = '', *args, **kwargs) -> str:
    print(f'{datetime.now().strftime('%H:%M:%S')} : {text}')
