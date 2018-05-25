# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 12:06:03 2016

@author: ss546418
"""

import urllib.request
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import numpy as np
C=0
B=[]
D=0



J=[]
work_day=[]
E=[]
K=0
to=datetime.date(2016, 1, 1)
'''
程式起始點
=========
try except沒測試

'''
for r in range(1095):
     to=to+datetime.timedelta(days=-1)
     if to.weekday()<5:
          E.append(str(to))
for j in E[:5]:
     F=[]
     A=[]
     url='http://www.taifex.com.tw/chinese/3/3_2_2.asp'
     url=url+'?'+'qtype=2&commodity_id=TXO&commodity_id2=&goday=&dateaddcnt=0&DATA_DATE_Y='+j[:4]+'&DATA_DATE_M='+j[5:7]+'&DATA_DATE_D='+j[8:10]+'&syear='+j[:4]+'&smonth='+j[5:7]+'&sday='+j[8:10]+'&datestart='+j[:4]+'%2F'+j[5:7]+'%2F'+j[8:10]+'&commodity_idt=TXO&commodity_id2t=&commodity_id2t2='
     html_data=urllib.request.urlopen(url).read()
     soup = BeautifulSoup(html_data,"html.parser")
     soup1=soup.select('.table_c tr td')
     if soup1==[]:
          print(str(j)+'非為交易日')
          continue
     else:
          for i in range(len(soup1)):
               J=soup1[i].text.strip()
               A.append(J)
               if (i+1) %17==0:
                    A[10]=A[10].replace('\n','')
                    A[10]=A[10].replace('\r','')
                    A[10]=A[10].replace('\t','')
                    A[10]=A[10].replace('▲','')
                    A[10]=A[10].replace('▼','')
                    A[9]=A[9].replace('▲','')
                    A[9]=A[9].replace('▼','')
                    F.append(A)
                    A=[]
          K=pd.DataFrame(F)
          K=pd.DataFrame(F,columns=['symbol','exp_d','strike','type','open','high','low','close','exp_c','rang','rang_c','vol','oi','B_b','B_s','H_b','H_s'])
          K.to_excel('data.xlsx','Sheet'+str(i))
##          K.to_pickle(j[:4]+j[5:7]+j[8:10]) #to pickle file
          print('成功下載日期為'+j+'的資料')
          work_day.append(j[:4]+j[5:7]+j[8:10])
     time.sleep(np.random.randint(0,2))
f = open("date.txt", "w")
f.write("\n".join(map(lambda x: str(x), work_day)))
f.close()
print('成功寫入txt檔')


'''
url='http://www.taifex.com.tw/chinese/3/3_2_1.asp'
