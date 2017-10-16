from blockchain import blockexplorer
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

blk = blockexplorer.get_latest_block()

c = complexity(blk.hash)
hashes = 2**c

print("leading bits the hash: ", c)
print("number of hashes     : ", hashes)

hours_of_work = hashes / miner_hashrate_per_h
print("hours of work:         ", '{:,.0f}'.format(hours_of_work))

electricity_kw = hours_of_work * miner_power_w_h / 1000
print("kWatts:                ", '{:,.0f}'.format(electricity_kw))

electricity_price = electricity_price_kW * electricity_kw
print("electricity bill, USD: ", '{:,.0f}'.format(electricity_price))



print("------------ let's have a look at the last 24h: (hash, timestamp, electricity bill for the block)")

blk = blockexplorer.get_block(blk.hash)
latestTimestamp = datetime.fromtimestamp(blk.time)
total_electricity_price = 0

while (latestTimestamp - datetime.fromtimestamp(blk.time)).total_seconds() < 24 * 60 * 60:
    c = complexity(blk.hash)
    hashes = 2 ** c
    hours_of_work = hashes / miner_hashrate_per_h
    electricity_kw = hours_of_work * miner_power_w_h / 1000
    electricity_price = electricity_price_kW * electricity_kw
    print("%s, %s, %s" % (blk.hash, datetime.fromtimestamp(blk.time).ctime(),  '{:,.0f}'.format(electricity_price)))

    total_electricity_price += electricity_price
    blk = blockexplorer.get_block(blk.previous_block)

print("total electricity bill for 24h, USD: ", '{:,.0f}'.format(total_electricity_price))


