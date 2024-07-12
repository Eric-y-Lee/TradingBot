# import websocket, json, pprint

# def on_open(ws):
#     print('socket opened')
#     msg = {
#         'type': 'subscribe',
#         'channels': [
#             {
#                 'name': 'ticker',
#                 'product_ids':['BTC-USD']
#             }
#         ]
#     }
#     ws.send(json.dumps(msg))

# def on_message(ws, message):
#     json_message = json.loads(message)
#     pprint.pprint(json_message)

# socket = "wss://ws-feed.pro.coinbase.com"
# ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
# ws.run_forever()
import coinbasepro as cbp
import pprint

public_client = cbp.PublicClient()

pprint.pprint(public_client.get_product_historic_rates('BTC-USD')[0])
pprint.pprint(public_client.get_product_historic_rates('BTC-USD')[1])
