import pandas as pd
import pandas_ta as ta
from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()

client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET"))

def obtener_datos_mercado(par, intervalo="15m", limite=100):
    klines = client.get_klines(symbol=par, interval=intervalo, limit=limite)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
    ])
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    df = df.astype(float)
    return df

def generar_indicadores(df):
    df['ema20'] = ta.ema(df['close'], length=20)
    df['ema50'] = ta.ema(df['close'], length=50)
    df['rsi'] = ta.rsi(df['close'], length=14)
    macd = ta.macd(df['close'])
    df['macd'] = macd['MACD_12_26_9']
    df['macd_signal'] = macd['MACDs_12_26_9']
    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    return df

def generar_senal(df, fase):
    df = generar_indicadores(df)
    ultima = df.iloc[-1]

    senal = None
    info = {'precio': ultima['close']}

    if fase == 1:
        if (ultima['ema20'] > ultima['ema50'] and
            45 < ultima['rsi'] < 60 and
            ultima['macd'] > ultima['macd_signal']):
            senal = 'compra'
    elif fase == 2:
        if ultima['ema20'] > ultima['ema50'] > ultima['ema20'].shift(1):
            senal = 'compra'
    elif fase in [3, 4]:
        if ultima['rsi'] < 30:
            senal = 'compra'
        elif ultima['rsi'] > 70:
            senal = 'venta'

    return senal, info

def seleccionar_mejor_par():
    try:
        tickers = client.get_ticker()  # o también client.ticker_price(), client.ticker_24hr()
        pares_validos = [x for x in tickers if x['symbol'].endswith('USDT') and float(x['quoteVolume']) > 5000000]

        mejores = sorted(pares_validos, key=lambda x: float(x['priceChangePercent']), reverse=True)[:10]

        for par_data in mejores:
            par = par_data['symbol']
            df = obtener_datos_mercado(par)
            if not df.empty:
                return par, df
        return None, None
    except Exception as e:
        print(f"Error en seleccionar_mejor_par: {e}")
        return None, None

