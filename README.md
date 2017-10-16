# py-bitcoin
A simple estimator of bitcoin's electricity bill

Bitcoin network consumes a lot of energy to mine blocks. The idea is to estimate the price of mining.

I assume that the whole world mines with the best miner I found, Antminer S9 (is it so?):
it costs $2000 (not important here), does 14Th/s and consumes 1372Watt/hour.

The bold assumption is that to find a hash with, namely, 74 leading zero bits
(like `000000000000000000374128dc19fa1a47d37b798105e8f54b696bd5daca0afe`)
you need `2^74 = 18889465931478580854784` hashes to check.
This assumption is challenged by the practical observations,
as it suggests that all the hashes within a day should have the same amount of leading zero bits.
It's not so.
E.g. adjacent blocks `0000000000000000000590d60e05a1ab8746a40b29a3c693613ddf1d5627a7ea` and
`000000000000000000c508bc2ada8ebc62cf1c69cb66a163d9a99abad87599b6` are 7 minutes away, yet the latter has 5 zero bits more (!)

If there's a better way to estimate, please let me know.

The cheapest price I found is $0.048 in China.

Please check out main.py and sample output for the rest.

Useful links:
* https://digiconomist.net/bitcoin-energy-consumption
* google



