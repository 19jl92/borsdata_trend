import pandas as pd
import requests
import numpy as np
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
df_stockPricesList = pd.read_csv("dataseries.csv", sep=';', decimal=',')
std_log_returns = []
mean_log_returns = []

c_returns = np.log(df_stockPricesList.c / df_stockPricesList.c.shift(1))
c_returns = c_returns.rename(index='c_returns', inplace=True)
df_stockPricesList = pd.concat([df_stockPricesList, c_returns], axis=1, join='inner')

#for i in df_stockPricesList.columns[1:]:
#    df_stockPricesList[i] = np.log(df_stockPricesList[i] / df_stockPricesList[i].shift(1))
#    std_log_returns.append(np.std(df_stockPricesList[i])*np.sqrt(252))
#    mean_log_returns.append(np.mean(df_stockPricesList[i])*252)
#print(mean_log_returns)