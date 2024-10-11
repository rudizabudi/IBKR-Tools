import yfinance as yf

type CoreObj = 'CoreObj'


def calculate_beta(symbol: str, core: CoreObj) -> float | None:

    result = {}
    try:
        bench_hist = yf.Ticker(core.benchmark).history(period=core.beta_period)
        bench_hist['Change'] = bench_hist['Close'].pct_change()
        variance = bench_hist['Change'].var()
        result['bench_current_price'] = float(round(bench_hist.iloc[-1]['Close'], 2))

        stock_hist = yf.Ticker(symbol).history(period=core.beta_period)
        stock_hist['Change'] = stock_hist['Close'].pct_change()
        core.underlying_prices[symbol] = float(round(stock_hist.iloc[-1]['Close'], 2))

        covariance = stock_hist['Change'].cov(bench_hist['Change'])
        beta = covariance / variance

        beta = float(round(beta, 3))

        return beta

    except ValueError:
        return None

if __name__ == '__main__':
    test = ['PYPL', 'NEE', 'NEM', 'ABR']
    for x in test:
        print(x, calculate_beta(x))