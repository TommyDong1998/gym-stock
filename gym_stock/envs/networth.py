from datetime import date
import yfinance as yf
import numpy as np
class NetWorth:
    def __init__(self,balance,symbols,start,end):
        self.balance=balance
        self.symbols=symbols
        self.lastOpen=None
        self.stocks=[0]*len(symbols)
        try:
            self.stockHistory=yf.download(self.symbols, start=start, end=end)
        except Exception:
            print("Exception: could not download")

    def set(self, stocks,date):
        prices=self.getOpen(date)
        if prices is None:
            print("No prices available. Cannot buy.")
            return
        stocks=np.array(stocks,dtype=float)
        buy=np.subtract(stocks,self.stocks)
        buy*=prices
        if np.sum(buy)>self.balance:
            return -1
        self.balance-=np.sum(buy)
        self.stocks=stocks
        return 1

    def calc(self,date):
        try:
            return self.balance + np.sum(self.stocks * self.getOpen(date))
        except Exception:
            print("Could not calc balance.")

        return self.balance
        
    def getOpen(self,date):
        try:
            self.lastOpen=self.stockHistory.loc[date.strftime("%Y-%m-%d")]["Open"].values
            return self.lastOpen
        except Exception:
            if self.lastOpen is not None:
                return self.lastOpen
            else:
                return None