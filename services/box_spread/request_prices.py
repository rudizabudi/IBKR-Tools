from datetime import datetime, timedelta
from functools import partial
from time import sleep
import yfinance as yf

from ibapi.contract import Contract as ibContract

from services.tws_api import TWSCon, TWSConDistributor
from core import ReqId, CoreDistributor, Core, RequestState


class ContractPrices:
    UPDATE_TIMER: int = 15  # in mins to consider a price out of date

    tws_con = None
    core = None

    prices: dict[ibContract, dict[str, datetime | float]] = {}

    @classmethod
    def request_price_tws(cls, contract: ibContract):
        # Lazy init at runtime
        if cls.core is None:
            cls.core: Core = CoreDistributor.get_core()

        if not cls.check_update(contract, datetime.now()):
            cls.core.threading_events['bxs_reqHistoricalData'].set()
            return

        if cls.tws_con is None:
            cls.tws_con: TWSCon = TWSConDistributor.get_con()

        if contract in cls.prices.keys():
            dt_dif = datetime.now() - cls.prices[contract][0]
            if dt_dif < timedelta(minutes=cls.UPDATE_TIMER):
                return

        price_callback = partial(cls.set_price, contract=contract)

        query_time = datetime.today().strftime("%Y%m%d-%H:%M:%S")
        duration_str = '1 D' #f'{cls.UPDATE_TIMER * 60} S'
        bar_size = f'{cls.UPDATE_TIMER} mins'

        if contract.secType == 'BAG':
            wts = 'BID_ASK'
        else:
            wts = 'TRADES'

        cls.tws_con.reqHistoricalData( reqId=ReqId.register_reqId(price_callback),
                                       contract=contract,
                                       endDateTime=query_time,
                                       durationStr=duration_str,
                                       barSizeSetting=bar_size,
                                       whatToShow=wts,
                                       useRTH=1,
                                       formatDate=1,
                                       keepUpToDate=False,
                                       chartOptions=[])

        print(f'Price requested for {contract}')

    @classmethod
    def request_price_yf(cls, index_contract: ibContract):
        # Lazy init at runtime
        if cls.core is None:
            cls.core: Core = CoreDistributor.get_core()

        if not cls.check_update(index_contract, datetime.now()):
            cls.core.threading_events['bxs_reqHistoricalData'].set()
            return

        resp = yf.Ticker(index_contract.yf_symbol)
        data = {'date': datetime.fromtimestamp(resp.info['regularMarketTime']), 'close': resp.info['regularMarketPrice']}
        cls.set_price(price=data, contract=index_contract)

        cls.core.threading_events['bxs_contract_price_received'].set()
        cls.core.threading_events['bxs_contract_price_received'].wait()

    @classmethod
    def set_price(cls, price: dict[str, str | float], contract: ibContract):
        if not isinstance(price['date'], datetime):
            price['date'] = datetime.strptime(price['date'], '%Y%m%d  %H:%M:%S')

        if contract in cls.prices.keys():
            if cls.prices[contract]['date'] >= price['date']:
                return

        cls.prices[contract] = { 'last_request': datetime.now(),
                                 'date': price['date'],
                                 'price': float(price['close'])
                                }

    @classmethod
    def check_update(cls, contract: ibContract, dt: datetime) -> bool:
        if contract not in cls.prices.keys():
            return True
        if cls.prices[contract]['last_request'] <= dt - timedelta(minutes=cls.UPDATE_TIMER):
            return True

        return False

    @classmethod
    def get_price(cls, contract: ibContract) -> float:
        return cls.prices[contract]['price']



