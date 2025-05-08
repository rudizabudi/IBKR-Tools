import requests
import pandas as pd

bs_type: str = 'Lend'  # 'Lend' or 'Borrow'
duration = 256

lower_strike = 5_500
upper_strike = 6_500

data = requests.get('https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/all/202410?type=daily_treasury_yield_curve&field_tdr_date_value_month=202410&page&_format=csv')

risk_free_rates = [x.split(',') for x in data.text.splitlines()][:2]

for i, x in enumerate(risk_free_rates[0][1:], start=1):
    risk_free_rates[0][i] = int(x.split(' ')[0].replace('\"', '')) * (30 if 'Mo"' == x.split(' ')[1] else 360)

risk_free_rates = {int(k): float(v) for k, v in zip(risk_free_rates[0][1:], risk_free_rates[1][1:])}

lower_dte = max([m for m in sorted(risk_free_rates.keys()) if m <= duration])
upper_dte = min([m for m in sorted(risk_free_rates.keys()) if m >= duration])

lower_yield = risk_free_rates[lower_dte]
upper_yield = risk_free_rates[upper_dte]

interpolated_yield = (lower_yield + ((duration - lower_dte) / (upper_dte - lower_dte)) * (upper_yield - lower_yield)) / 100

print(f"The risk free rate for {duration} days is: {interpolated_yield * 100:.2f}%")

