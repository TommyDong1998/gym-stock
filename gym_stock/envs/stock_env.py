import gym
from datetime import date
import datetime
import numpy as np
from gym import spaces
from gym_stock.envs.networth import NetWorth

class StockEnv(gym.Env):
    def __init__(self):
        print('Environment initialized')

        #stock info
        self.symbols=["MSFT","AAPL","GOOG","FB"]
        self.startDate=date.fromisoformat('2020-01-09')
        self.endDate=date.fromisoformat('2021-03-01')
        #reinforcement actions
        self.initialBalance=1000
        self.lastBalance=self.initialBalance
        self.action_space=spaces.Tuple([spaces.Discrete(3) for i in self.symbols])
        self.observation_space = spaces.MultiDiscrete([10000 for i in self.symbols])
        #spaces.Discrete(10000)
        self.reset()

    def getState(self):
        try:
            return np.array(self.net.getOpen(self.currDate)).astype(int)
        except Exception:
            print("Could not get state")
        return [999]*len(self.symbols)

    def getBalance(self):
        return int(self.net.calc(self.currDate))
    def step(self,action):
        #if you lost half your money .... you fked up
        if self.currDate>=self.endDate:
            self.done=True
        balance=self.getBalance()
        if balance<self.initialBalance/2:
            self.done=True

        #0=hold 1=buy if possible 2=sell if possible
        stockAmt=[]
        for indx,i in enumerate(action):
            if i==2:
                stockAmt.append(0)
            elif i==0:
                stockAmt.append(self.net.stocks[indx])
            else:
                stockAmt.append(1)
        bought=1
        
        #while we have enough money to buy
        while bought!=-1 and np.sum(stockAmt)>0:
            bought=self.net.set(stockAmt,self.currDate)
            stockAmt=np.multiply(stockAmt,2)
        
        state=self.getState()
        #increment date and calculate gains
        self.currDate += datetime.timedelta(days=1)
        gains=balance-self.lastBalance
        self.lastBalance=balance
        #observation, reward, done, info
        self.render()
        return state, gains, self.done, {}

    def render(self):
        print("Balance",self.getBalance())

    def reset(self):
        print('Environment reset')
        self.done=False
        self.currDate=self.startDate
        self.net=NetWorth(self.initialBalance,self.symbols,self.startDate, self.endDate)
        return self.getState()
