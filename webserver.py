from flask import Flask, request, abort, jsonify
import time, json, asyncio, aiohttp, re, traceback, os
from flask_socketio import SocketIO, emit, join_room, disconnect, ConnectionRefusedError
from datetime import datetime, timedelta
RATE_LIMIT_WINDOW = timedelta(seconds=60)
RATE_LIMIT_COUNT = 10
app = Flask(__name__)
webhook = "WEBHOOKHERE"
cookie = "COOKIEHERE"
socketio = SocketIO(app, async_mode="eventlet")
numClients = 0
connectedClients = {}
accounts = {}
ddos = False
with open("items.json", "r") as f: 
  ids = json.load(f)
items = ids
prev_items = ids
joins_per_second = 0
join_count = 0
start_time = time.time()
alreadyFound = []
ban_list = []
rate_limit_data = {}
joins_per_second = 0

url_list = [
    'https://catalog.roproxy.com/v2/search/items/details?Category=1&salesTypeFilter=2&SortType=3&Subcategory=2&MaxPrice=0&Limit=10/',
    'https://catalog.roproxy.com/v1/search/items/details?Category=11&Subcategory=19&CurrencyType=3&MaxPrice=0&salesTypeFilter=2&SortType=3&limit=30/',
    'https://catalog.roproxy.com/v2/search/items/details?Category=1&SortType=3&salesTypeFilter=2&Subcategory=2&MaxPrice=0&Limit=10/',
    'https://catalog.roproxy.com/v2/search/items/details?Category=1&SortType=3&salesTypeFilter=2&MaxPrice=0&Subcategory=2&Limit=10/',
    'https://catalog.roproxy.com/v1/search/items/details?Category=11&SortType=3&Subcategory=19&CurrencyType=3&MaxPrice=0&salesTypeFilter=2&limit=30/',
    'https://catalog.roproxy.com/v2/search/items/details?Category=1&SortType=3&salesTypeFilter=2&MaxPrice=0&Limit=10&Subcategory=2/',
    'https://catalog.roproxy.com/v1/search/items/details?SortType=3&Category=11&Subcategory=19&CurrencyType=3&MaxPrice=0&salesTypeFilter=2&limit=30/',
    'https://catalog.roproxy.com/v1/search/items/details?SortType=3&Subcategory=19&Category=11&CurrencyType=3&MaxPrice=0&salesTypeFilter=2&limit=30/',
    'https://catalog.roproxy.com/v2/search/items/details?Category=1&SortType=3&Subcategory=2&salesTypeFilter=2&MaxPrice=0&Limit=10/',
    'https://catalog.roproxy.com/v1/search/items/details?SortType=3&CurrencyType=3&Subcategory=19&Category=11&MaxPrice=0&salesTypeFilter=2&limit=30/',
    'https://catalog.roproxy.com/v2/search/items/details?Category=1&SortType=3&Subcategory=2&MaxPrice=0&salesTypeFilter=2&Limit=20/',
    'https://catalog.roproxy.com/v2/search/items/details?Category=1&SortType=3&Subcategory=2&MaxPrice=0&salesTypeFilter=2&Limit=100/',
    'https://catalog.roproxy.com/v1/search/items/details?MaxPrice=0&SortType=3&Category=11&salesTypeFilter=2&CurrencyType=3&Subcategory=19&limit=28/',
    'https://catalog.roproxy.com/v1/search/items/details?SortType=3&Category=11&salesTypeFilter=2&MaxPrice=0&CurrencyType=3&Subcategory=19&limit=28/',
    'https://catalog.roproxy.com/v2/search/items/details?Category=1&SortType=3&Subcategory=2&MaxPrice=0&salesTypeFilter=2&Limit=101389120830100/',
    'https://catalog.roproxy.com/v2/search/items/details?Category=1&Subcategory=2&SortType=3&MaxPrice=0&salesTypeFilter=2&Limit=10/',
    'https://catalog.roproxy.com/v1/search/items/details?MaxPrice=0&CurrencyType=3&SortType=3&Category=11&salesTypeFilter=2&Subcategory=19&limit=28/',
    'https://catalog.roproxy.com/v2/search/items/details?Category=1&salesTypeFilter=2&Subcategory=2&SortType=3&MaxPrice=0&Limit=10/',
    'https://catalog.roproxy.com/v2/search/items/details?Category=1&salesTypeFilter=2&SortType=3&Subcategory=2&MaxPrice=0&Limit=10/',
    'https://catalog.roproxy.com/v1/search/items/details?MaxPrice=0&salesTypeFilter=2&CurrencyType=3&SortType=3&Category=11&limit=28/',
    'https://catalog.roproxy.com/v1/search/items/details?MaxPrice=0&salesTypeFilter=2&CurrencyType=3&SortType=3&Category=11&limit=10/'
]



  
                     

def ban_user(user_id):
    ban_list.append(user_id)

     
@socketio.on('connect')
def handle_connect():
  try:
    global numClients
    global connectedClients
    numClients += 1
    try:
      pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
      ipAddress = re.findall(pattern, request.headers.get('X-Forwarded-For'))[-1]
      if ipAddress in ban_list:
        print(f"{ipAddress} attempted a DDoS attack")  
        disconnect()
      if ipAddress in connectedClients:
        print("ban")
        disconnect()
      else:
        connectedClients[ipAddress] = 1
    except Exception as e: print(e); return
    print('A user connected')

    socketio.emit('user_joined', {'users': numClients})
    socketio.emit('new_auto_search_items', {'message': 'New item data received', 'data': items})
  except Exception as e:
    print(e)
    pass

  
@socketio.on('disconnect')
def handle_disconnect():
  try:
    global numClients
    global connectedClients
    pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    ipAddress = re.findall(pattern, request.headers.get('X-Forwarded-For'))[-1]
    print(f"{ipAddress} disconnect")
    if ipAddress in connectedClients: del connectedClients[ipAddress]
    numClients -= 1
    socketio.emit('user_disconnected', {'users': numClients})
    socketio.emit('new_auto_search_items', {'message': 'New item data received', 'data': items})
  except: pass

async def send_webhook():
  connector = aiohttp.TCPConnector(limit=None)  # Increase concurrent connections
  async with aiohttp.ClientSession(connector=connector) as session:
    while True:
        print(f"Number of currently connected clients: {numClients}")
        payload = {
            'content': f'Number of currently connected clients: {numClients}, VERSION: 2.0.0'
        }
        response = await session.post(webhook, headers={'Content-Type': 'application/json'}, json=payload)
        if not response.ok:
            print(f"Error sending webhook: {response.text}")
        await asyncio.sleep(10)
            
    
            
async def auto_searcho():
    global items, prev_items
    rang = 2
    async with aiohttp.ClientSession() as client:
        tries = 0
        url = "https://catalog.roblox.com/v1/search/items/details?Category=11&salesTypeFilter=1&SortType=3&IncludeNotForSale=True&Limit=30"
        current_cursor = None
        iretations = 0
        while True:
            try:
                for i in range(rang):
                    async with client.get(f"{url}&cursor={current_cursor}" if not current_cursor is None else url, cookies={".ROBLOSECURITY": cookie}, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                        "Referer": "https://www.roblox.com/account/settings/security"
                    }) as response:
                        print(response.status, iretations, rang, current_cursor)
                        j = await response.json()
                        if response.status == 429: await asyncio.sleep(5); continue
                        assert response.status == 200, await response.json()
                        print("+")
                        if not j['nextPageCursor']: break
                        current_cursor = j['nextPageCursor']
                        for item in j['data']:
                            if (item.get('priceStatus', "nyet") == "Off Sale" and not item.get("unitsAvailableForConsumption") and "unitsAvailableForConsumption" not in item and not item.get("saleLocationType", "g") == "ExperiencesDevApiOnly" and item.get('price', 0) == 0 and str(item['id']) not in items):
                                print(item['id'])      
                                items[f"{item['id']}"] = {"current_buys": 0, "max_buys": float('inf'), "max_price": 0}
                                with open("items.json", "w") as f: json.dump(items, f, indent=4)
                                print({f"{item['id']}": item})
                                async with client.post(webhook, json={"content": f"https://www.roblox.com/catalog/{item['id']}/XOLO-WATCHER"}) as r: pass
                    items = {str(key): value for key, value in items.items()}
                    print(len(items))
                    await asyncio.sleep(5)

                if prev_items != items:
                    changed_items = []
                    for item_id, item_data in items.items():
                        if item_data != prev_items.get(item_id):
                            changed_items.append(item_id)

                    if changed_items:
                        changed_items_string = "\n".join(['"{}"'.format(item) for item in changed_items])
                        print("Items list has changed. Changed item IDs:\n{}".format(changed_items_string))

                        print(items)
                prev_items = items
                rang = 2
                current_cursor = None
                iretations += 1
                if iretations % 2 == 0:
                  url = "https://catalog.roblox.com/v1/search/items/details?Category=11&salesTypeFilter=1&SortType=3&IncludeNotForSale=True&Limit=30"
                  print("url 1")
                else:
                  url = "https://catalog.roblox.com/v1/search/items/details?Keyword=orange%20teal%20cyan%20red%20green%20topaz%20yellow%20wings%20maroon%20space%20dominus%20lime%20mask%20mossy%20wooden%20crimson%20salmon%20brown%20pastel%20%20ruby%20diamond%20creatorname%20follow%20catalog%20link%20rare%20emerald%20chain%20blue%20deep%20expensive%20furry%20hood%20currency%20coin%20royal%20navy%20ocean%20air%20white%20cyber%20ugc%20verified%20black%20purple%20yellow%20violet%20description%20dark%20bright%20rainbow%20pink%20cyber%20roblox%20multicolor%20light%20gradient%20grey%20gold%20cool%20indigo%20test%20hat%20limited2%20headphones%20emo%20edgy%20back%20front%20lava%20horns%20water%20waist%20face%20neck%20shoulders%20collectable&Category=11&salesTypeFilter=1&SortType=3&IncludeNotForSale=True&Limit=30"
                  print("url 2")
                await asyncio.sleep(10)
            except aiohttp.client_exceptions.ServerDisconnectedError:
              print("server disconnected"); continue
            except Exception as e:
                current_cursor = None
                tries += 1
                if tries == 1:
                    
                    rang = 2
                print(f"An error occurred: {e}")
                traceback.print_exc()
              
  
@app.route('/items', methods=['POST'])
def items_site():
    return items


async def starto():
    tasks = []
    tasks.append(send_webhook())
    tasks.append(auto_searcho())
    await asyncio.gather(*tasks, asyncio.to_thread(socketio.run, app, host='0.0.0.0', port=8080))


asyncio.run(starto())
