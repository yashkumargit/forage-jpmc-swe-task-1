# ################################################################################
# #
# #  Permission is hereby granted, free of charge, to any person obtaining a
# #  copy of this software and associated documentation files (the "Software"),
# #  to deal in the Software without restriction, including without limitation
# #  the rights to use, copy, modify, merge, publish, distribute, sublicense,
# #  and/or sell copies of the Software, and to permit persons to whom the
# #  Software is furnished to do so, subject to the following conditions:
# #
# #  The above copyright notice and this permission notice shall be included in
# #  all copies or substantial portions of the Software.
# #
# #  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# #  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# #  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# #  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# #  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# #  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# #  DEALINGS IN THE SOFTWARE.
#
# import json
# import random
# import urllib.request
#
# # Server API URLs
# QUERY = "http://localhost:8080/query?id={}"
#
# # 500 server request
# N = 500
#
#
# def getDataPoint(quote):
#     """ Produce all the needed values to generate a datapoint """
#     """ ------------- Update this function ------------- """
#     stock = quote['stock']
#     bid_price = float(quote['top_bid']['price'])
#     ask_price = float(quote['top_ask']['price'])
#     price = bid_price
#     return stock, bid_price, ask_price, price
#
#
# def getRatio(price_a, price_b):
#     """ Get ratio of price_a and price_b """
#     """ ------------- Update this function ------------- """
#     return 1
#
#
# # Main
# if __name__ == "__main__":
#     # Query the price once every N seconds.
#     for _ in iter(range(N)):
#         quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())
#
#         """ ----------- Update to get the ratio --------------- """
#         for quote in quotes:
#             stock, bid_price, ask_price, price = getDataPoint(quote)
#             print("Quoted %s at (bid:%s, ask:%s, price:%s)" % (stock, bid_price, ask_price, price))
#
#         print("Ratio %s" % getRatio(price, price))
import json
import random
import urllib.request

# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# 500 server request
N = 500


def getDataPoint(quote):
    """ Produce all the needed values to generate a datapoint """
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    price = (bid_price + ask_price) / 2  # Use the average of bid and ask price for the stock price
    return stock, bid_price, ask_price, price


def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b """
    if price_b == 0:
        return None  # Handle division by zero if price_b is 0
    return price_a / price_b


# Main
if __name__ == "__main__":
    # Query the price once every N seconds.
    for _ in iter(range(N)):
        try:
            quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())
        except urllib.error.URLError as e:
            print(f"Failed to reach the server. Reason: {e.reason}")
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

        prices = {}

        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            prices[stock] = price
            print("Quoted %s at (bid:%s, ask:%s, price:%s)" % (stock, bid_price, ask_price, price))

        # Assuming 'stock_a' and 'stock_b' are the keys for the stocks we want to compare
        if 'stock_a' in prices and 'stock_b' in prices:
            ratio = getRatio(prices['stock_a'], prices['stock_b'])
            if ratio is not None:
                print("Ratio %s" % ratio)
            else:
                print("Ratio could not be calculated due to division by zero.")
