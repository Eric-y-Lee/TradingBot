import websocket, json, pprint
import talib
import numpy
import config

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = ''
TRADE_QUANTITY = 1

closed = []
in_position = False

def on_open(ws):
    print("opened")
    auth_data = {
        "action": "auth", 
        "key": config.API_KEY, 
        "secret": config.API_SECRET_KEY
        }
    ws.send(json.dumps(auth_data))

    listen_msg = {"action": "subscribe",  
                  "bars": ["NVDA"]}

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
    print(closed)

# Doji Alg
    if (close >= open) and (open - close > 0.1):
        print("we will buy")
    # if (open - close > 0.01):
    #     print("we will buy")
    # eg. 170 then take profit at 171.7 at1% increase

    if len(closed) < RSI_PERIOD:
        np_closed = numpy.array(closed)
        # rsi = talib.RSI(np_closed, RSI_PERIOD)
        # print(f'most recent rsi value: {rsi}')
        # last_rsi = rsi[-1]
        # print(f'current rsi is {last_rsi}')

    #     if last_rsi > RSI_OVERBOUGHT:
    #         if in_position is False:
    #             print("No not have any position!")
    #         else:
    #             print("Stock Overbought! Time to Sell!")
    #             in_position = True

    #     if last_rsi < RSI_OVERSOLD:
    #         if in_position:
    #             print("Already holding that stock")
    #         else:
    #             print("Stock Oversold! Time to buy!")
    #             in_position = True
    
socket = "wss://stream.data.alpaca.markets/v2/iex"
ws = websocket.WebSocketApp(socket, on_open=on_open, on_close = on_close, on_message=on_message)
ws.run_forever()