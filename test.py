import websocket, json, pprint
import talib as ta
import numpy as np
import config

file1 = open("output.txt","a")

closed = [1330.95, 1334.65, 1340, 1338.7, 1234.1, 12344, 1123, 12554, 125524, 124, 
          155124, 1234, 55125, 15125, 125566, 12315, 125515, 1666, 677235, 6234,
          12455, 1244, 5124, 5515, 6347, 23445, 12334, 125512, 1330.95, 1334.65,
          1340, 1338.7, 1234.1, 12344,
          1232]

closed = np.array(closed)
print(closed)
macd, signal, macdHist = ta.MACD(closed)
rsi = ta.RSI(closed)
print(f'rsi: {rsi}')
print(macd, signal, macdHist)
print(f'This is macd {macd[-1]}')
print(f'This is signal {signal[-1]}')
print(f'This is hist {macdHist[-1]}')
print(macd[-2], macd[-1])