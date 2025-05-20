from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()

client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET"))

def obtener_capital_total():
    try:
        balances = client.get_account()['balances']
        total_usdt = 0.0
        for asset in balances:
            symbol = asset['asset']
            free = float(asset['free'])
            if free > 0:
                if symbol == 'USDT':
                    total_usdt += free
                else:
                    try:
                        ticker = client.get_symbol_ticker(symbol=f"{symbol}USDT")
                        precio = float(ticker['price'])
                        total_usdt += free * precio
                    except:
                        continue
        return round(total_usdt, 2)
    except Exception as e:
        print(f"Error al obtener el capital total: {e}")
        return 0.0

def determinar_fase(capital):
    if capital < 20:
        return 1
    elif capital < 100:
        return 2
    elif capital < 1000:
        return 3
    else:        
        return 4
