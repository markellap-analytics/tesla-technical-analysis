import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style 
import pandas as pd
import yfinance as yf
import numpy as np
style.use('ggplot')


import os
os.makedirs('plots', exist_ok=True)

#Downloading Data from Yahoo
start=dt.datetime(2014,1,2)
end=dt.datetime(2024,10,31)
df=yf.download('TSLA', start, end)

print(df.head())
print(df.head(10))
print(df.tail())
print(df.tail(10))

#Choose Adjusted Close if availabl, else Close
if 'Adj Close' in df.columns:
    df['Price']=df['Adj Close']
else:
    df['Price']=df['Close']

df.to_csv('TSLA_raw.csv')

#Calculating log returns:
df['Log_Ret'] = np.log(df['Price'] / df['Price'].shift(1))

print(df.tail()['Log_Ret'])

#Αnnualized volatility:
df['Volatility'] = df['Log_Ret'].rolling(window=252).std()*np.sqrt(252)

print(df.head())
print(df.tail())

#Save that data in file:
df.to_csv('TSLA.csv')
df[['Price','Volatility']].plot(subplots=True, color='blue', figsize=(8,6))
plt.savefig('plots/volatility.png')
plt.show()
plt.close()

#SMA & EMA
df['SMA50']=df['Price'].rolling(window=50).mean()
df['SMA200']=df['Price'].rolling(window=200).mean()

plt.figure(figsize=(10, 6))
plt.plot(df['Price'], label='Price', alpha=0.7)
plt.plot(df['SMA50'], label='50-Day SMA', color='red')
plt.plot(df['SMA200'],label='200-Day SMA', color='green')
plt.title('Tesla Stock with Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.savefig('plots/price_sma.png')
plt.show()
plt.close()

#Daily Returns Distribution
plt.figure(figsize=(8,5))
df['Log_Ret'].hist(bins=100, alpha=0.7)
plt.title('Distribution of Tesla Daily Log Returns')
plt.xlabel('Log Return')
plt.ylabel('Frequency')
plt.savefig('plots/ret_distr.png')
plt.show()
plt.close()

#Cumulative Returns
df['Cumulative_Returns']=(1+df['Log_Ret']).cumprod()

plt.figure(figsize=(10,6))
df['Cumulative_Returns'].plot()
plt.title('Cumulative Returns of Tesla Stock (2014-2024)')
plt.ylabel('Growth of 1$ Investment')
plt.xlabel('Date')
plt.savefig('plots/cumul_ret.png')
plt.show()
plt.close()

#Volatily vs Price
fig,ax1=plt.subplots(figsize=(10,6))

ax1.set_xlabel('Date')
ax1.set_ylabel('Price (USD)',color='blue')
ax1.plot(df['Price'], color='blue', label='Price')
ax1.tick_params(axis='y', labelcolor='blue')

ax2=ax1.twinx()
ax2.set_ylabel('Volatility', color='red')
ax2.plot(df['Volatility'], color='red',alpha=0.6, label='Volatility')
ax2.tick_params(axis='y', labelcolor='red')

plt.title('Tesla Price vs Volatility')
plt.savefig('plots/volatxprice.png')
plt.show()
plt.close()

#Sharpe Ratio
mean_return=df['Log_Ret'].mean()*252
volatility=df['Log_Ret'].std()*np.sqrt(252)
sharpe_ratio=mean_return/volatility

print(f'Annualized Sharpe Ration: {sharpe_ratio:.2f}')