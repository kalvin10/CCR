#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from datetime import datetime
df1= pd.read_excel('PSP_Jan_Feb_2019.xlsx')
drop_list=[]
for i in range(len(df1)-1):
 if df1.loc[i,'country']==df1.loc[i+1,'country'] and df1.loc[i,'amount']==df1.loc[i+1,'a
 dt1 = df1.loc[i,'tmsp']
 dt2 = df1.loc[i+1,'tmsp']
 delta=dt2-dt1
 if delta.seconds<=60:
 drop_list.append(i) 


# In[2]:





# In[3]:





# In[ ]:





# In[ ]:




