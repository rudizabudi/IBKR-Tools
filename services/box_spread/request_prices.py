from datetime import datetime, timedelta
from functools import partial, partialmethod
from time import sleep
import yfinance as yf

from ibapi.contract import Contract as ibContract

from services.tws_api import TWSCon, TWSConDistributor
from core import ReqId, CoreDistributor, Core, RequestState


class IndexPrice:
    UPDATE_TIMER: int = 5  # in mins to consider a price out of date

    tws_con = None
    core = None

    last_prices: dict[ibContract, dict[str, datetime | float]] = {}

    @classmethod
    def request_price_tws(cls, index_contract: ibContract):
        if not cls.check_update(index_contract, datetime.now()):
            return

        # Lazy init at runtime
        if cls.tws_con is None:
            cls.tws_con: TWSCon = TWSConDistributor.get_con()

        if cls.core is None:
            cls.core: Core = CoreDistributor.get_core()

        if index_contract in cls.last_prices.keys():
            dt_dif = datetime.now() - cls.last_prices[index_contract][0]
            if dt_dif < timedelta(minutes=cls.UPDATE_TIMER):
                return

        price_callback = partial(cls.set_price, contract=index_contract)

        cls.tws_con.request_end['historicalData'] = RequestState.REQUESTED

        wts = 'TRADES'
        query_time = datetime.today().strftime("%Y%m%d-%H:%M:%S")
        duration_str = f'{cls.UPDATE_TIMER * 60} S'
        bar_size = f'{cls.UPDATE_TIMER} mins'

        cls.tws_con.reqHistoricalData( reqId=ReqId.register_reqId(price_callback),
                                       contract=index_contract,
                                       endDateTime=query_time,
                                       durationStr=duration_str,
                                       barSizeSetting=bar_size,
                                       whatToShow=wts,
                                       useRTH=0,
                                       formatDate=1,
                                       keepUpToDate=False,
                                       chartOptions=[])

        while cls.tws_con.request_end['historicalData'] != RequestState.RECEIVED:
            sleep(.1)

        cls.core.threading_events['bxs_contract_price_received'].set()
        print(f'Index price requested for {index_contract}')


    @classmethod
    def request_price(cls, index_contract: ibContract):
        if not cls.check_update(index_contract, datetime.now()):
            return

        # Lazy init at runtime
        if cls.core is None:
            cls.core: Core = CoreDistributor.get_core()

        resp = yf.Ticker(index_contract.yf_symbol)
        data = {'date': datetime.fromtimestamp(resp.info['regularMarketTime']), 'close': resp.info['regularMarketPrice']}
        cls.set_price(price=data, contract=index_contract)

        cls.core.threading_events['bxs_contract_price_received'].set()

    @classmethod
    def set_price(cls, price: dict[str, str | float], contract: ibContract):
        if not isinstance(price['date'], datetime):
            price['date'] = datetime.strptime(price['date'], '%Y%m%d  %H:%M:%S')

        cls.last_prices[contract] = {'last_request': datetime.now(),
                                     'date': price['date'],
                                     'price': float(price['close'])
                                     }

        print(f'{cls.last_prices[contract]}')

    @classmethod
    def check_update(cls, contract: ibContract, dt: datetime):
        if contract not in cls.last_prices.keys():
            return True
        if cls.last_prices[contract]['last_request'] <= dt - timedelta(minutes=cls.UPDATE_TIMER):
            return True

        return False

    @classmethod
    def get_price(cls, contract: ibContract) -> float:
        return cls.last_prices[contract]['price']


