import config

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest, GetOrdersRequest
from alpaca.trading.enums import AssetClass
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus

import pandas as pd 
import numpy as np 
import matplotlib as mpl
from tabulate import tabulate

class AlpacaAPI:
    def __init__(self) -> None:
        self.trading_client = TradingClient(config.API_KEY, config.API_SECRET_KEY, paper = True)

    def menu(self):
        # Get our account information.
        account = self.trading_client.get_account()
        # Check if our account is restricted from trading.
        if account.trading_blocked:
            print('Account is currently restricted from trading.')

        # Check how much money we can use to open new positions.
        print('${} is available as buying power.'.format(account.buying_power))

        # Check our current balance vs. our balance at the last market close
        balance_change = float(account.equity) - float(account.last_equity)
        print(f'Today\'s portfolio balance change: ${balance_change}')

            # # Get a list of all of our positions.
        portfolio = self.trading_client.get_all_positions()
        for stocks in portfolio:
            print(stocks.symbol, stocks.qty, stocks.current_price, stocks.avg_entry_price, stocks.change_today)

        request_params = GetOrdersRequest(status=QueryOrderStatus.OPEN,)
        self.orders = self.trading_client.get_orders(request_params)

    def buy_stock(self):
         # preparing orders
        self.market_order_data = MarketOrderRequest(
                            symbol="AAPL",
                            qty=1,
                            side=OrderSide.BUY,
                            time_in_force=TimeInForce.DAY
                            )

        # Market order
        self.market_order = self.trading_client.submit_order(
                        order_data= self.market_order_data
                    )

    def order(self):
        symbol_array = []
        quantity_array= []
        orderType_array = []
        orderSide_array = []

        if len(self.orders)==0:
            print("NO OPEN ORDERS")
        else:
            for order in reversed(self.orders):
                symbol_array.append(order.symbol)
                quantity_array.append(order.qty)
                orderType_array.append(order.type.split(' ')[0].strip())
                orderSide_array.append(order.side.split(' ')[0])
                # print(order.symbol, order.qty, order.type, order.side, order.limit_price, order.stop_price, order.submitted_at)
            df = pd.DataFrame({
                        "SYMBOL": symbol_array,
                        "Quantity": quantity_array,
                        "Order Type": orderType_array,
                        "Order Request": orderSide_array
                    })
            print(tabulate(df, headers = 'keys', tablefmt='psql', showindex = False))

        # trading_client.cancel_orders()

"""
    What to do:
        I need to use Web socket from the Alpaca API to get the real-time price of the stock
        Then use the Doji algorithm to buy and sell the stock. 
        I'm thinking using the minute bar and then calculate when to sell and buy

        Eventually, I think I can create an AI model to train with a lot of data of a specific stock 
        so that depending on the factors, it will take the most profit. 
        Such as like on this volume and MCD and RSI line, it will sell and buy. 
        This will be automated.
"""
            