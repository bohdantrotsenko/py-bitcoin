import json, requests
from datetime import datetime

miner_hashrate_per_s = 14 * 1000 * 1000 * 1000 * 1000 # Antminer S9 does 14 TH/s
miner_hashrate_per_h = miner_hashrate_per_s * 60 * 60 # TH/hour, respectively

miner_power_w_h = 1372       # watts/hour for Antminer S9
electricity_price_kW = 0.048 # in USD, China, cheapest I've found

def leading_bits(c: chr):
    'number of leading (0) bits in a hex char'
    if (c >= '0') and (c <= '7'):
        if c < '4':
            if c < '2':
                if c == '0':
                    return 4
                else:
                    return 3
            else:
                return 2
        else:
            return 1
    else:
        return 0
def complexity(hash: str):
    'number of leading 0 bits in a sha256 hash'
    bits = (leading_bits(c) for c in hash)
    sum = 0
    for b in bits:
        sum += b
        if b != 4:
            break
    return sum

url = 'https://blockchain.info/blocks/?format=json'
print('downloading', url)
json_data=requests.get(url).content
data = json.loads(json_data.decode('utf-8'))

print("LB = number of leading bits; PRICE = estimated price to mine the block")
print("hash                                                             LB     PRICE timestamp")

total = 0
min = -1
count = 0
for blk in data['blocks']:
    if blk['main_chain']:
        c = complexity(blk['hash'])
        hashes = 2**c
        hours_of_work = hashes / miner_hashrate_per_h
        electricity_kw = hours_of_work * miner_power_w_h / 1000
        electricity_price = electricity_price_kW * electricity_kw
        total += electricity_price
        if (electricity_price < min) or (min < 0):
            min = electricity_price
        print(blk['hash'], c, '{:>9,.0f}'.format(electricity_price), datetime.fromtimestamp(blk['time']).ctime())
        count = count + 1

print("electricity bill, USD: ", '{:,.0f}'.format(total))
interval_span_days = (data['blocks'][0]['time'] - data['blocks'][-1]['time']) / 24 / 60 / 60
print("time mining, days    : ", '{:,.4f}'.format(interval_span_days))
per_day = total / interval_span_days
print("est. per day, USD    : ", '{:,.0f}'.format(per_day))

print("----- using (min price of block) * (number of blocks):")
total2 = min * count
print("electricity bill, USD: ", '{:,.0f}'.format(total2))
per_day2 = total2 / interval_span_days
print("est. per day, USD    : ", '{:,.0f}'.format(per_day2))
