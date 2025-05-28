from collections import defaultdict
from services.beta_weighted_deltas.positions import Position


class StockCache:
    betas: defaultdict[Position, float] = defaultdict(float)
    underlying_prices: defaultdict[Position, float] = defaultdict(float)

    @classmethod
    def get_beta(cls, symbol: str) -> float:
        for pos in cls.betas.keys():
            if pos.get_symbol() == symbol:
                return cls.betas[pos]

        raise Exception(f'No beta found for symbol {symbol}')

    @classmethod
    def get_price(cls, symbol: str) -> float:
        for pos in cls.underlying_prices.keys():
            if pos.get_symbol() == symbol:
                return cls.underlying_prices[pos]

        raise Exception(f'No price found for symbol {symbol}')

