from datetime import datetime
import pandas as pd
import os
from readresearchroundup import roundup
from findvolume import avgvoldf

#grab today's date and turn it into a string
date = datetime.now()
date = date.strftime('%Y%m%d')
date = '20231229'

#load current price and volume data
current_price_volume_traded = pd.read_csv(f"NASDAQ_{date}.csv")
cpdf = current_price_volume_traded[['Symbol', 'Close', 'Volume']]
cpdf = cpdf.rename(columns={'Symbol': 'Ticker'})
print(cpdf)
#load target data from research roundup files
targetdf = pd.DataFrame()

for file in os.listdir():
    if file.endswith(".txt"):
        pddf = roundup(file)
        targetdf = targetdf._append(pddf, ignore_index=True)
    else:
        continue

#load volume data from all NASDAQ files to find average volume:
volumedf = pd.DataFrame()

for file in os.listdir():
    if file.endswith(".csv"):
        vdf = avgvoldf(file)
        volumedf = volumedf._append(vdf, ignore_index=True)
    else:
        continue
volumedf = volumedf.groupby(['Symbol'], as_index=False).mean()
volumedf=volumedf.rename(columns={'Symbol':'Ticker'})



#drop duplicates and calculate mean for duplicate Ticker and Date combinations
targetdf = targetdf.drop_duplicates()
targetdf = targetdf.groupby(['Ticker', 'Date'], as_index=False).mean()

#merge both dataframes into one large dataframe and create another dataframe for maxes
finaldf = pd.merge(cpdf, targetdf, on='Ticker', how='left')
maxdf = pd.DataFrame()
finaldf['Volume'] = volumedf['Volume']
#find expected return for a stock as a percent and then rate it against other expected returns to return a value between 0 and 1
finaldf['Expected Earnings Per Share'] = (finaldf['New Target Price']-finaldf['Close']) / finaldf['Close']
expected_earnings_max = finaldf['Expected Earnings Per Share'].max()
maxdf['Expected Earnings Per Share'] = finaldf['Expected Earnings Per Share'] / expected_earnings_max
finaldf['Expected Earnings Per Share'] = finaldf['New Target Price']-finaldf['Close']

#find the optimism percent by change in target price and then rate it against other optimism percents to give each stock a value between 0 and 1
finaldf['Optimism Percent'] = ((finaldf['New Target Price'] - finaldf['Old Target Price']) / finaldf['Old Target Price'])*100
optimism_percent_max= finaldf['Optimism Percent'].max()
maxdf['Optimism Percent'] = finaldf['Optimism Percent']/optimism_percent_max

#give each volume a score between 0 and 1 with 1 being most traded
max_vol = finaldf['Volume'].max()
maxdf['Volume'] = (finaldf['Volume'] / max_vol)**0.2

#linear combo to give a "score" for each stock
finaldf['Rating'] = 1.5*maxdf['Optimism Percent'] + 2*maxdf['Expected Earnings Per Share'] + maxdf['Volume']
max_score = finaldf['Rating'].max()
finaldf['Rating'] = (finaldf['Rating'] / max_score) * 100
finaldf = finaldf.sort_values(by='Rating', ascending=False)

#get rid of decimals to make ratings easier to read
finaldf['Rating'] = finaldf['Rating'].round(0)

#use top 10 stocks for The Simple NASDAQ Index
simple_index = finaldf.head(10)
print(simple_index)
