import logging
from kiteconnect import KiteConnect
import csv
import time                   
from datetime import datetime
import os

api_key = "k8jfisczsz5bsbff"
access_token = "UmA3Rg35iByJmlzL8U1UygUGuR5KqJPE"
base_directory = r"C:\Users\ashwi\OneDrive\Desktop\kiteToCSV\CSVfiles"
#data = kite.generate_session("request_token_here", api_secret="your_secret")  acces toekn will expire every day so try to use request token
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

json_data = [{"tradingview":"NIFTY251230C26050","exchange":"NFO","zerodha":"NIFTY25DEC26050CE","token":16798978,"lot":75},
{"tradingview":"NIFTY251230P26100","exchange":"NFO","zerodha":"NIFTY25DEC26100PE","token":16800770,"lot":75},
{"tradingview":"BANKNIFTY251230C59100","exchange":"NFO","zerodha":"BANKNIFTY25DEC59100CE","token":13162498,"lot":35},
{"tradingview":"BANKNIFTY251230P59200","exchange":"NFO","zerodha":"BANKNIFTY25DEC59200PE","token":13163778,"lot":35},
{"tradingview":"BSX260101C85100","exchange":"BFO","zerodha":"SENSEX2610185100CE","token":296575749,"lot":20},
{"tradingview":"BSX260101P85200","exchange":"BFO","zerodha":"SENSEX2610185200PE","token":296571141,"lot":20},
{"tradingview":"BTCUSDT","exchange":"CRYPTO","zerodha":"BTCUSD","token":99999999,"lot":1}]

#kite api needs token in list format from json_data
tokens = [item['token'] for item in json_data]

try:
    while True:
        try:
            live_quotes = kite.ltp(tokens)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            today_date = now.strftime("%Y-%m-%d")

            folder_path = os.path.join(base_directory, today_date)
            os.makedirs(folder_path, exist_ok=True)
            
            for item in json_data:
                token_str = str(item['token'])
                if token_str in live_quotes:
                    symbol_name = item['tradingview']
                    file_name = os.path.join(folder_path, f"{symbol_name}.csv")

                    row_data = {
                            "timestamp": current_time,
                            "tradingview": symbol_name,
                            "exchange": item['exchange'],
                            "token": item['token'],
                            "last_price": live_quotes[token_str]['last_price'],
                            "lot": item['lot']
                        }
                    file_exists = os.path.isfile(file_name)
                    #save to csv
                    try:
                        with open(file_name, 'a', newline='') as f:
                            writer = csv.DictWriter(f, fieldnames=row_data.keys())

                            if not file_exists:
                                writer.writeheader()
                            writer.writerow(row_data)
                    except PermissionError:
                        print(f"Warning: Close {symbol_name}.csv in Excel to update!")
                

                    
            print(f"[{current_time}] CSV updated successfully.")
        except Exception as api_err:
            print(f"Error: {api_err}. Retrying...")
    

        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped by user.")
except Exception as e:
    print(f"Error: {e}")


#add a retry mechanim in case httpconn fails (done)
#csv file wont update if i have the file  (added warning)

