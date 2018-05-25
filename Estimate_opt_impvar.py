# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 13:09:06 2016

@author: user
"""
import numpy as np
import pandas as pd
import statistics as st
import matplotlib.pyplot as plt
import datetime as dt
import xlrd
from scipy import stats
from sklearn.metrics import mean_squared_error




def r_excl(f):
    data=pd.read_excel(f+'.xlsx',sheetname='Sheet1')
    return data

def CorP(S,K,T,r,sigma,t):
    if str(t)=='Call':  #call
        return bs_c(S,K,T,r,sigma)
    else:
        return bs_p(S,K,T,r,sigma)

def bs_c(S,K,T,r,sigma):
    d1=(np.log(S/K)+(r+ 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2=(np.log(S/K)+(r- 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    value=(S*stats.norm.cdf(d1,0.0,1.0)-K*np.exp(-r*T)*stats.norm.cdf(d2,0.0,1.0))
    return value

def bs_p(S,K,T,r,sigma):
    d1=(np.log(S/K)+(r+ 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2=(np.log(S/K)+(r- 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    value=K*np.exp(-r*T)*stats.norm.cdf(-d2,0.0,1.0)-stats.norm.cdf(-d1,0.0,1.0)*S
    return value

def vega(S,K,T,r,sigma):
    d1=(np.log(S/K)+(r+ 0.5*sigma**2)*T)/(sigma*T**0.5)
    vega=S*stats.norm.cdf(d1,0.0,1.0)*T**0.5
    return vega

'''
讀出時間檔轉list
===============
list A 為交易時間 可用reverse 做轉換
'''


'''
read其中一日資料
==============
astype把type做轉換
且拋棄vol==0的行
'''
##B=pd.read_pickle(t[0]) #A[0]為20151231 如轉換年為A[0][:4]
##Date_now=dt.date(int(A[0][:4]),int(A[0][4:6]),int(A[0][6:8]))

def third_wen(y):  #找出結算日
     day=21-(dt.date(int(y[0:4]),int(y[4:6]),1).weekday()+4)%7
     return dt.date(int(y[0:4]),int(y[4:6]),day)
    
def str_date(t): #轉換str為日期
    T=dt.date(int(t[:4]),int(t[4:6]),int(t[6:8]))
    return T

def three_type(a):  #0表無資料 1表次近月 2表次進月 3表遠月
    if a<5/365:
        return 0
    elif a<=30/365:
        return 1
    elif a<=60/365:
        return 2
    else:
        return 3
    
def t_p(ty,S0,K):
    if ty=='Call':
        if S0/K >=1.06:
            d=-2         #深價內
        elif S0/K >=1.03:
            d=-1
        elif S0/K >=0.97:
            d=0
        elif S0/K >=0.94:
            d=1
        else:
            d=2           #深價外
    if ty=='Put':
        if S0/K >=1.06:
            d=2          #深價外         
        elif S0/K >=1.03:
            d=1
        elif S0/K >=0.97:
            d=0
        elif S0/K >=0.94:
            d=-1
        else:
            d=-2         #深價內
    
    return d
'''
正式測試
======
'''
rolday=90    #滾動天數(歷史)

#讀取txt檔，裏頭有著交易日
Call1M1=[]
Call1M2=[]
Call1M-1=[]
Call1M-2=[]
Put1M1=[]
Put1M2=[]
Put1M-1=[]
Put1M-2=[]

Call2M1=[]
Call2M2=[]
Call2M-1=[]
Call2M-2=[]
Put2M1=[]
Put2M2=[]
Put2M-1=[]
Put2M-2=[]

Call3M1=[]
Call3M2=[]
Call3M-1=[]
Call3M-2=[]
Put3M1=[]
Put3M2=[]
Put3M-1=[]
Put3M-2=[]


t=[]
file=open('work_dat.txt','r')
t=file.read().split('\n')


#分別讀入指數及
TWindex=r_excl('TWindex')
TWindex['Lreturn']=np.log(TWindex.close/TWindex.close.shift(1))
TWindex['std']=TWindex['Lreturn'].rolling(window=rolday).std()*252**0.5
TWindex['HL']=TWindex['high']-TWindex['low']
#抓前200算歷史波動度





TXO=pd.read_pickle(t[0])
TXO.vol=TXO.vol.astype(int)
TXO=TXO.loc[TXO.vol!=0]
TXO=TXO[TXO['exp_d'].map(len)==6]
TXO['exp']=TXO['exp_d'].map(third_wen)
TXO['T']=(((TXO['exp']-str_date(t[0]))/ np.timedelta64(1, 'D')).astype(int))*(1/365)  #轉換time.delata to int
TXO['3type']=(TXO['T'].map(three_type)).astype(int)
TXO=TXO.loc[TXO['3type']!=0]
#將周選篩除
TXO['S']=TWindex['close'][0]
TXO['r']=0.0135 #定存一個月利率
TXO['h_var']=TWindex['std'][rolday+1]


#implied var
TXO.S=TXO.S.astype(float)
TXO.strike=TXO.strike.astype(float)
TXO.close=TXO.close.astype(float)
##可用
TXO['exp_c']=TXO['exp_c'].astype(float)
TXO['pp']=np.vectorize(t_p)(TXO['type'], TXO['S'],TXO['strike'])
TXO['his']=np.vectorize(CorP)(TXO['S'], TXO['strike'],TXO['T'],TXO['r'],TXO['h_var'],TXO['type'])
TXO['spread']=abs(TXO['his']-TXO['exp_c']).astype(float)
#print(TXO)
##print(TXO[['exp_d','strike','S','type','close','his','spread']])
#print(TXO[(TXO['pp']==-2)|(TXO['type']=='call')]['spread'].mean())
#print(TXO[(TXO['pp']==0)|(TXO['type']=='call')]['spread'])
RMSE = mean_squared_error(TXO[(TXO['pp']==0)|(TXO['type']=='call')|(TXO['3type']==1)]['his'],TXO[(TXO['pp']==0)|(TXO['type']=='call')|(TXO['3type']==1)]['close'])**0.5
#print(TWindex[['Lreturn','HL']].describe())
print(RMSE)

C1M
















#    return logL

