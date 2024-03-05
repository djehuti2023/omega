# Import du module Metatrader5
import MetaTrader5 as mt5
import time
# Importer le module 'pandas' pour afficher les données
# obtenues sous forme de tableau
import pandas as pd
import requests
import numpy as np
from datetime import datetime

import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind(("192.168.1.3", 8888))
serversocket.listen(10)

symbol = "EURUSD"

msg = "\0"

# Les liens vers le serveur
url_m1 = 'http://192.168.1.3:6666/v1/act/m1'
url_m5 = 'http://192.168.1.3:6666/v1/act/m5'
url_m15 = 'http://192.168.1.3:6666/v1/act/m15'

timeframe_m1 = mt5.TIMEFRAME_M1
timeframe_m5 = mt5.TIMEFRAME_M5
timeframe_m15 = mt5.TIMEFRAME_M15

# Obtenir les donnees du marche
def get_rates(timeframe):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 11)
    rates_frame = pd.DataFrame(rates)
    df = rates_frame

    # supprimer les colonnes time et  real_volume  des dataframes
    df.drop('time', inplace=True, axis=1)
    df.drop('real_volume', inplace=True, axis=1)

    # Isoler les colonnes des dataframes
    open_m1 = df['open'].to_numpy()
    high_m1 = df['high'].to_numpy()
    low_m1 = df['low'].to_numpy()
    close_m1 = df['close'].to_numpy()
    tick_volume_m1 = df['tick_volume'].to_numpy()
    spread_m1 = df['spread'].to_numpy()
    
    # construction du tableau de donnees
    array = np.array([open_m1,high_m1,low_m1,close_m1,tick_volume_m1,spread_m1])
    
    return array

# Ouvrir une position buy
def open_buy():
    # ouvrir une position buy
    # les parametres pour la prise de position
    lot = 0.1
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 20
    sl = price - 50 * point
    tp = price + 50 * point

    # la requete d'une position Buy
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": 234000,
        "comment": "ouverture de position buy",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # envoie une demande de prise de position
    result = mt5.order_send(request)

    return result

# Ouvrir une position sell
def open_sell():
    # Ouvrir une position sell
    lot = 0.1
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 20
    sl = price + 50 * point
    tp = price - 50 * point
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": 234001,
        "comment": "ouverture de position sell",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    
    # envoie une demande de trading
    result = mt5.order_send(request)

    return result


# fermer les positions buy
def close_buy(position):

    tick = mt5.symbol_info_tick(position.symbol)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "position": position.ticket,
        "symbol": position.symbol,
        "volume": position.volume,
        "type": mt5.ORDER_TYPE_SELL,
        "price": tick.bid,  
        "deviation": 20,
        "magic": 100,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    # si la fermeture echoue
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("order_send a échoué, retcode={}".format(result.retcode))
        print("   résultat",result)
    else:
        # Au cas ou la fermeture reussi
        print("Position #{} fermée, {}".format(position.ticket,result))
    return 0


# fermer les positions sell
def close_sell(position):

    tick = mt5.symbol_info_tick(position.symbol)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "position": position.ticket,
        "symbol": position.symbol,
        "volume": position.volume,
        "type": mt5.ORDER_TYPE_BUY,
        "price": tick.ask,  
        "deviation": 20,
        "magic": 100,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    # si la fermeture echoue
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("order_send a échoué, retcode={}".format(result.retcode))
        print("   résultat",result)
    else:
        # Au cas ou la fermeture reussi
        print("Position #{} fermée, {}".format(position.ticket,result))

    return 0


"""
 def get_open_positions(symbol=None):
    
    # get the list of positions on symbols whose names contain "*USD*"
    usd_positions=mt5.positions_get()
    if usd_positions==None:
        df=None
        print("Aucune position n'est ouverte  code de l'erreur ={}".format(mt5.last_error()))
    elif len(usd_positions)>0:
 
        # Affiche ces positions sous forme de table pandas.Dataframes
        df=pd.DataFrame(list(usd_positions),columns=usd_positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id','magic','swap','profit','comment','identifier','time','price_open','sl','tp','price_current','symbol','reason','volume'], axis=1, inplace=True)

    return df
 """


if __name__ == "__main__":
    while True:

        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()
        
        array_m1 = get_rates(timeframe_m1)
  
        data_m1 = {'observation':array_m1.tolist()}

        response_m1 = requests.post(url_m1,json=data_m1)

        print("Les requetes sont envoyes")
        now = datetime.now()

        print("#################################################")
        print("")
        current_time = now.strftime("%H:%M:%S")
        print("Temps actuele =", current_time)
        print("")
        print(response_m1.json())

        print("")
        print("#################################################")
        
        # Recueillons le conteneu de la requete
        d_m1 = response_m1.json()

        # les signaux envoyes par le serveur
        signal_m1 = d_m1['action_de_M1'][0][0]
        
        # obtenir les postions ouvertes
        positions = mt5.positions_get()
        
       
        try:
            connection, addr = serversocket.accept()
            print("[INFO]\t Connexion etablie:", addr)            
            msg = connection.recv(1024).decode()
            print("[INFO]\t Message:", msg)

        except ValueError:
            connection, addr = serversocket.accept()
            print("[INFO]\t Connexion etablie:", addr)
            msg = connection.recv(1024).decode()
            print("[INFO]\t Message:", msg)
        
        # dissossier les signaux MA
        msg_array = msg.split(",")
        signal_ma_m1 = int(msg_array[0])
        signal_ma_m5 = int(msg_array[1])
        signal_ma_m15 = int(msg_array[2])
        

        # si les signaux sont tous buy
        if signal_m1 > 0.6 and signal_ma_m1 == 0 and signal_ma_m5 == 0 and signal_ma_m15 == 0:
            for position in positions:
                # Fermer les positions sell
                if(position.type == 1):
                    close_sell(position)
                    pass

            # ouvrons une position buy
            result = open_buy()
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Order_send a échoué, retcode={}".format(result.retcode))
            else:
                print("################### Buy ouverte ###########################")
        elif signal_m1 < 0 and signal_m1 >= -0.6 and signal_ma_m1 == 1 and signal_ma_m5 == 1 and signal_ma_m15 == 1:
            
            for position in positions:
                # fermer les positions buy
                if(position.type == 0):            
                    close_buy(position)
                    pass

            result = open_sell()
            # vérifie le résultat de l'exécution
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Order_send a échoué, retcode={}".format(result.retcode))
            else:
                print("################ Sell ouverte ##############################")
        else:
            print("Aucun bon signal pour le moment")
        

        # Fermer les connexions venant du socket
        #connection.close()
        #serversocket.close()

        time.sleep(60)