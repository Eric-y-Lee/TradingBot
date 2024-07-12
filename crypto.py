import websocket, json, pprint
import talib as ta
import numpy as np
import config

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest, GetOrdersRequest
from alpaca.trading.enums import AssetClass
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus


RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = ''
TRADE_QUANTITY = 1

closed = []
in_position = False
portfolio = []
trading_client = TradingClient(config.API_KEY, config.API_SECRET_KEY, paper = True)

def on_open(ws):
    print("opened")
    auth_data = {
        "action": "auth", 
        "key": config.API_KEY, 
        "secret": config.API_SECRET_KEY
        }
    ws.send(json.dumps(auth_data))

    listen_msg = {"action": "subscribe",
                   "bars": ["BTC/USD"]}

    # listen_msg = {"action": "subscribe",  
    #               "trades": ["NVDA"],
    #               "quotes":["NVDA"],
    #               "bars":["*"]}

    ws.send(json.dumps(listen_msg))

def on_close(ws):
    print('closed connection')

def on_message(ws,message):
    # print(message)
    json_message = json.loads(message)
    pprint.pprint(json_message)

    open = json_message[0]['o']
    close = json_message[0]['c']
    
    print(f"'Open:; {open}, 'Close:' {close}")
    closed.append(close)
    print(len(closed))

# Doji Alg
    # if (close >= open) and (open - close > 0.1):
    #     print("we will buy")
    # if (open - close > 0.01):
    #     print("we will buy")
    # eg. 170 then take profit at 171.7 at1% increase

    if len(closed) > RSI_PERIOD:
        np_closed = np.array(closed)
        rsi = ta.RSI(np_closed, RSI_PERIOD)
        # print(f'most recent rsi value: {rsi}')    
        last_rsi = rsi[-1]
        print(f'current rsi is {last_rsi}')

        if last_rsi > 69:
            print("This crypto is overbought. Should we sell?")
            # print("Stock Overbought! Time to Sell!")

            # if in_position:
            #     print("Stock Overbought! Time to Sell!")
            # else:
            #     print("No not have any position!")
            #     in_position = False

            market_order_sell = MarketOrderRequest(
                symbol = 'BTC/USD',
                # qty = 0.001,
                notional = 1000.00,
                side = OrderSide.SELL,
                # type = OrderType.MARKET,
                time_in_force = TimeInForce.GTC,
            )
            res = trading_client.submit_order(order_data = market_order_sell)

        if last_rsi < 31:
            print("This crypto is oversold. Should we buy?")

            # print("Stock Oversold! Time to buy!")

            # if in_position:
            #     print("Already holding that stock")
            # else:
            #     print("Stock Oversold! Time to buy!")
            #     in_position = True
            market_order_buy = MarketOrderRequest(
                symbol = 'BTC/USD',
                # qty = 0.001,
                notional = 1000.00,
                side = OrderSide.BUY,
                # type = OrderType.MARKET,
                time_in_force = TimeInForce.GTC,
            )
            market_order = trading_client.submit_order(order_data = market_order_buy)
    
    # need 34 data for MACD
    # need 34 to compare previous MACD and signal indicators
        if len(closed) > 33:
            # np_closed2 = np.array(closed)
            macd, signal_line, macd_histogram = ta.MACD(np_closed)
            print(f'This is macd {macd[-1]}')
            print(f'This is signal {signal_line[-1]}')
            print(f'This is hist {macd_histogram[-1]}')

        if len(closed) > 34 :
            if (macd[-2] > signal_line[-2] and signal_line[-1] > macd[-1]) or (macd[-2] < signal_line[-2] and macd[-1] > signal_line[-1]):
                print("The signal and MACD has intersected")
                #  or rsi[-2] < 30 or rsi[-3] < 30
                if last_rsi < 31:
                    print("TIME TO BUY!")
                    portfolio.append(close)
                    print(portfolio)
                #  or rsi[-2] > 70 or rsi[-3] > 70
                if last_rsi > 69:
                    print("time to SELL")
                    portfolio.append(open)
                    print(portfolio)
# when the crypto is decreasing, the signal is closer to 0 
# and when stock is increasing, macd is closer to 0  

socket = "wss://stream.data.alpaca.markets/v1beta3/crypto/us"
ws = websocket.WebSocketApp(socket, on_open=on_open, on_close = on_close, on_message=on_message)
ws.run_forever()