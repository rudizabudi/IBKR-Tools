from datetime import datetime
from dotenv import load_dotenv
import os

from services.contracts import Position

type ContractInstance = 'ContractInstance'
type SubPageInstance = 'SubPageInstance'
type QtObj = 'QtObj'
type QTFunc = 'QTFunc'
load_dotenv('.env_dev_live')

if os.getenv('DEV_VAR') == 'rudizabudi':
    load_dotenv('.env_dev_live')
else:
    load_dotenv('.env')

class Core:
    def __init__(self):
        self.host_ip: str = os.getenv('HOST_IP')
        self.api_port: int = int(os.getenv('API_PORT'))
        #self.api_port: int = 7491
        self.client_id: int = int(os.getenv('CLIENT_ID'))
        self.account_id: str | None = os.getenv('ACCOUNT_ID') # TODO: Add selection popup if no account_Id provided

        self.benchmark: str = os.getenv('BENCHMARK')
        self.bench_pos: ContractInstance = Position(core=self, **{'contract': {
                                                                        'symbol': self.benchmark,
                                                                        'secType': 'STK',
                                                                        'currency': 'USD',
                                                                        'exchange': 'SMART'
                                                                    }})
        self.beta_period: str = os.getenv('BETA_PERIOD')

        self.reqId_hashmap: dict = {}
        self.reqId: int = 1

        self.account_list: list[str] = []

        self.frame_tabs: dict[str: SubPageInstance] = {}
        self.active_tab: str = ''

        self.raw_positions: dict[str, dict[str: any]] = {}

        self.positions: list[ContractInstance] = []
        self.positions_str_sorted: list[str] = []

        self.pos_betas: dict[str: float] = {}

        self.table_contents: dict[str: list[str | float]] = {}

        self.item_register: dict[str: QtObj] = {}
        self.underlying_prices: dict[str: float] = {}

        self.bwd_update_refresh: QTFunc = None

    def set_TWSCon(self, TWSCon):
        self.TWSCon = TWSCon


def tprint(text: str = '', *args, **kwargs):
    print(f'{datetime.now().strftime('%H:%M:%S')} : {text}')
