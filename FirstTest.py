from ib_insync import *
from stockstats import StockDataFrame as Sdf

# util.startLoop()  # uncomment this line when in a notebook
def myalgo(stock):
    signal = stock['macds']
    macd   = stock['macd'] 
    macdh = (macd - signal)

    print ("Lunghezza: " ,  len(signal))
    listLongShort = ["No data", "No data"]    # Since you need at least two days in the for loop
    for i in range(2, len(signal)):
        
        if (macdh[i]>macdh[i-1] and macdh[i-1]> macdh[i-2] and macdh[i-2]<0 and macdh[i-1]>0):
            listLongShort.append("BUY")
        elif (macdh[i]<macdh[i-1] and macdh[i-1]< macdh[i-2] and macdh[i-2]>0 and macdh[i-1]<0):
            listLongShort.append("SELL")    
        else:
            listLongShort.append("HOLD")

    print ("Fa il merge" , len(listLongShort))

    stock['Advice'] = listLongShort

    return stock

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=10)

contract = Stock('MSFT','SMART','USD', primaryExchange="NASDAQ")
bars = ib.reqHistoricalData(contract, endDateTime='', durationStr='166 D',
        barSizeSetting='1 day', whatToShow='TRADES', useRTH=True)

# convert to pandas dataframe:
df = util.df(bars)

stock  = Sdf.retype(df)
result = myalgo(stock)
print (result)
#print (df)
#print(df[['date', 'open', 'high', 'low', 'close','volume']])