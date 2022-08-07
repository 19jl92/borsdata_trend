import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt

#stock = [
#    "SE0000337842"
#    ]
#instruments = 'https://apiservice.borsdata.se/v1/instruments?authKey='
#content = requests.get(instruments, headers={'content-type': 'application/json'})
#data = content.json()['instruments']
#df_instruments = pd.DataFrame(data)
#df = df_instruments[df_instruments['isin'].isin(stock)] #sends list of true and false, true if isin matches
#df_instruments = df_instruments[['insId', 'isin', 'name', 'urlName']]
# ------------------------------------------------------------------------------------------------
#stockPrice = 'https://apiservice.borsdata.se/v1/instruments/'+str(df.iloc[0].insId)+'/stockprices?authKey=&maxCount=20'
#content2 = requests.get(stockPrice, headers={'content-type': 'application/json'})
#data3 = content2.json()['stockPricesList']
#df_stockPricesList = pd.DataFrame(data3)
#df_stockPricesList.dropna(inplace=True)
# ------------------------------------------------------------------------------------------------
#df_stockPricesList.to_csv("dataseries.csv", sep=';', index=False, decimal=',')

#d = {'col1': [1, 2], 'col2': [3, 4]}
#df = pd.DataFrame(data=d)

#print(df['col2'].shift(-1))
#

x=250
df_stockPricesList = pd.read_csv("dataseries.csv", sep=';', decimal=',')
df_stockPricesList["moving_average"] = df_stockPricesList['c'].rolling(window=x).mean()
df_stockPricesList.dropna(inplace=True)

df_stockPricesList["c_returns"] = np.log(df_stockPricesList.c / df_stockPricesList.c.shift(1))
df_stockPricesList["c_returns_shift"] = df_stockPricesList["c_returns"].shift(-1)
df_stockPricesList.dropna(inplace=True)

#-----
df_stockPricesList["new"] = np.where(df_stockPricesList['c'] > df_stockPricesList['moving_average'], df_stockPricesList.c_returns.shift(-1), 0)
df_stockPricesList.dropna(inplace=True)
df_stockPricesList["cum_c_returns_shift"] = np.cumprod(df_stockPricesList.c_returns_shift+1)
df_stockPricesList["cum_returns_new"] = np.cumprod(df_stockPricesList.new+1)
mean_cum_returns = np.mean(df_stockPricesList["c_returns"])*252
mean_cum_returns_new = np.mean(df_stockPricesList["new"])*252

#results[x][0] = float(x)
#results[x][1] = float(mean_cum_returns)
#results[x][2] = float(mean_cum_returns_new)
#results[x][3] = df_stockPricesList.cum_c_returns_shift.iloc[-1]
#results[x][4] = df_stockPricesList.cum_returns_new.iloc[-1]

#df_results =  pd.DataFrame(results, columns=['n', 'mean_cum_returns', 'mean_cum_returns_new', 'cum_c_returns_shift', 'cum_returns_new'], index=None)
#df_results.to_csv("dataseries3.csv", sep=';', index=False, decimal=',')

#-----------------------------------------------------
df_stockPricesList["d"] = df_stockPricesList["d"].astype("datetime64")
df_stockPricesList =df_stockPricesList.set_index("d")
plt.figure(figsize=(9, 5))
plt.plot(df_stockPricesList["cum_c_returns_shift"],  color='b', lw=0.8)
plt.plot(df_stockPricesList["cum_returns_new"],  color='r', lw=0.8)
plt.xlabel("Date")
plt.ylabel("Cum Returns")
plt.title("Time Series Plot")
plt.show()
