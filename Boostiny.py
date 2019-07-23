#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import pickle
import requests
import json
import import_ipynb
import pandas as pd


# In[4]:


login="aziz.bahri@boostiny.tn"
password="Boostiny2019"


# ## Session ID

# In[5]:


def get_session_id(login,password):
    r = requests.get('https://influencer.boostiny.app/scripts/server.php?D=%7B%22C%22%3A%22Pap_Api_AuthService%22%2C%22M%22%3A%22authenticate%22%2C%22fields%22%3A%5B%5B%22name%22%2C%22value%22%2C%22values%22%2C%22error%22%5D%2C%0D%0A%5B%22username%22%2C%22'+login+'%22%2Cnull%2C%22%22%5D%2C%0D%0A%5B%22password%22%2C%22'+password+'%22%2Cnull%2C%22%22%5D%0D%0A%2C%5B%22roleType%22%2C%22M%22%2Cnull%2C%22%22%5D%2C%5B%22language%22%2C%22en-US%22%2Cnull%2C%22%22%5D%2C%5B%22isFromApi%22%2C%22Y%22%2Cnull%2C%22%22%5D%2C%5B%22apiVersion%22%2C%22%22%2Cnull%2C%22%22%5D%5D%7D')
    df=pd.DataFrame(r.json())
    return df['fields'][7][1]


# ## Affiliates

# In[6]:


def get_all_affiliates(login,password):
    session=get_session_id(login,password)
    r = requests.get('https://influencer.boostiny.app/scripts/server.php?D=%7B%22C%22%3A%22Gpf_Rpc_Server%22%2C+%22M%22%3A%22run%22%2C+%22requests%22%3A%5B%7B%22C%22%3A%22Pap_Merchants_User_TopAffiliatesGrid%22%2C+%22M%22%3A%22getRows%22%2C+%22sort_col%22%3A%22name%22%2C+%22sort_asc%22%3Atrue%2C+%22offset%22%3A0%2C+%22limit%22%3A30%2C+%22columns%22%3A%5B%5B%22id%22%5D%2C%5B%22id%22%5D%2C%5B%22firstname%22%5D%2C%5B%22lastname%22%5D%2C%5B%22userid%22%5D%2C%5B%22username%22%5D%2C%5B%22dateinserted%22%5D%2C%5B%22data4%22%5D%2C%5B%22data9%22%5D%2C%5B%22data10%22%5D%2C%5B%22data11%22%5D%2C%5B%22salesCount%22%5D%2C%5B%22commissions%22%5D%5D%7D%5D%2C+%22S%22%3A%22'+session+'%22%7D')
    df=pd.DataFrame(r.json())
    limit=str(df["count"][0])
    i=0
    df=pd.DataFrame.from_dict(dict(df["rows"]))             
    final=pd.DataFrame(columns=list(df[0][0]))
    while i<int(limit):
        url='https://influencer.boostiny.app/scripts/server.php?D=%7B%22C%22%3A%22Gpf_Rpc_Server%22%2C+%22M%22%3A%22run%22%2C+%22requests%22%3A%5B%7B%22C%22%3A%22Pap_Merchants_User_TopAffiliatesGrid%22%2C+%22M%22%3A%22getRows%22%2C+%22sort_col%22%3A%22name%22%2C+%22sort_asc%22%3Atrue%2C+%22offset%22%3A'+str(i)+'%2C+%22limit%22%3A'+str(i+500)+'%2C+%22columns%22%3A%5B%5B%22id%22%5D%2C%5B%22id%22%5D%2C%5B%22firstname%22%5D%2C%5B%22lastname%22%5D%2C%5B%22userid%22%5D%2C%5B%22username%22%5D%2C%5B%22dateinserted%22%5D%2C%5B%22data4%22%5D%2C%5B%22data9%22%5D%2C%5B%22data10%22%5D%2C%5B%22data11%22%5D%2C%5B%22salesCount%22%5D%2C%5B%22commissions%22%5D%5D%7D%5D%2C+%22S%22%3A%22'+session+'%22%7D'
        r=requests.get(url)
        df=pd.DataFrame(r.json())
        df=pd.DataFrame.from_dict(dict(df["rows"]))
        df=pd.DataFrame(columns=list(df[0][0]),data=list(list(df[0][1:])))
        final=pd.concat([df,final],ignore_index=True)
        i+=500
    final.to_csv("recommender_system/affiliates.csv",index=False)


# In[7]:


get_all_affiliates(login,password)


# ## Banners

# In[6]:


def get_all_banners(login,password):
    session=get_session_id(login,password)
    r = requests.get('https://influencer.boostiny.app/scripts/server.php?D=%7B%22C%22%3A%22Gpf_Rpc_Server%22%2C+%22M%22%3A%22run%22%2C+%22requests%22%3A%5B%7B%22C%22%3A%22Pap_Merchants_Banner_BannersStatsGrid%22%2C+%22M%22%3A%22getRows%22%2C+%22sort_col%22%3A%22rorder%22%2C+%22sort_asc%22%3Atrue%2C+%22offset%22%3A0%2C+%22limit%22%3A30%2C+%22filters%22%3A%5B%5B%22rstatus%22%2C%22NE%22%2C%22Y%22%5D%2C%5B%22transactionstatus%22%2C%22IN%22%2C%22A%2CP%22%5D%5D%2C+%22columns%22%3A%5B%5B%22id%22%5D%2C%5B%22id%22%5D%2C%5B%22banner%22%5D%2C%5B%22rtype%22%5D%2C%5B%22isconfirmed%22%5D%2C%5B%22campaignname%22%5D%2C%5B%22account%22%5D%2C%5B%22description%22%5D%2C%5B%22dateinserted%22%5D%5D%7D%5D%2C+%22S%22%3A%22'+session+'%22%7D')
    df=pd.DataFrame(r.json())
    limit=str(df["count"][0])
    i=0
    df=pd.DataFrame.from_dict(dict(df["rows"]))
    final=pd.DataFrame(columns=list(df[0][0]))
    while i<int(limit):
        url='https://influencer.boostiny.app/scripts/server.php?D=%7B%22C%22%3A%22Gpf_Rpc_Server%22%2C+%22M%22%3A%22run%22%2C+%22requests%22%3A%5B%7B%22C%22%3A%22Pap_Merchants_Banner_BannersStatsGrid%22%2C+%22M%22%3A%22getRows%22%2C+%22sort_col%22%3A%22rorder%22%2C+%22sort_asc%22%3Atrue%2C+%22offset%22%3A' +str(i)+'%2C+%22limit%22%3A'+str(i+500)+'%2C+%22filters%22%3A%5B%5B%22rstatus%22%2C%22NE%22%2C%22Y%22%5D%2C%5B%22transactionstatus%22%2C%22IN%22%2C%22A%2CP%22%5D%5D%2C+%22columns%22%3A%5B%5B%22id%22%5D%2C%5B%22id%22%5D%2C%5B%22banner%22%5D%2C%5B%22rtype%22%5D%2C%5B%22isconfirmed%22%5D%2C%5B%22campaignname%22%5D%2C%5B%22account%22%5D%2C%5B%22description%22%5D%2C%5B%22dateinserted%22%5D%5D%7D%5D%2C+%22S%22%3A%22'+session+'%22%7D' 
        r=requests.get(url)
        df=pd.DataFrame(r.json())
        df=pd.DataFrame.from_dict(dict(df["rows"]))
        df=pd.DataFrame(columns=list(df[0][0]),data=list(list(df[0][1:])))
        final=pd.concat([df,final],ignore_index=True)
        final=final.drop(['isconfirmed','name','rtype'], axis=1)
        #final=final.loc[final.rstatus.isin(["A"])]
        i+=500
    final.to_csv("recommender_system/all_banners.csv",index=False)


# In[7]:


get_all_banners(login,password)


# ## Commision
# 

# In[8]:


def get_all_commisions(login,password):
    session=get_session_id(login,password)
    r = requests.get('https://influencer.boostiny.app/scripts/server.php?D=%7B%22C%22%3A%22Gpf_Rpc_Server%22%2C+%22M%22%3A%22run%22%2C+%22requests%22%3A%5B%7B%22C%22%3A%22Pap_Merchants_Transaction_TransactionsGrid%22%2C+%22M%22%3A%22getRows%22%2C+%22sort_col%22%3A%22dateinserted%22%2C+%22sort_asc%22%3Afalse%2C+%22offset%22%3A0%2C+%22limit%22%3A100%2C+%22filters%22%3A%5B%5B%22rstatus%22%2C%22IN%22%2C%22A%2CP%22%5D%2C%5B%22rtype%22%2C%22IN%22%2C%22C%2CS%22%5D%5D%2C+%22columns%22%3A%5B%5B%22id%22%5D%2C%5B%22id%22%5D%2C%5B%22commission%22%5D%2C%5B%22bannerid%22%5D%2C%5B%22name%22%5D%2C%5B%22rtype%22%5D%2C%5B%22tier%22%5D%2C%5B%22commissionTypeName%22%5D%2C%5B%22rstatus%22%5D%2C%5B%22userid%22%5D%5D%7D%5D%2C+%22S%22%3A%22'+session+'%22%7D')
    df=pd.DataFrame(r.json())
    limit=str(df["count"][0])
    i=0
    df=pd.DataFrame.from_dict(dict(df["rows"]))
    final=pd.DataFrame(columns=list(df[0][0]))
    while i<int(limit):
        url = 'https://influencer.boostiny.app/scripts/server.php?D=%7B%22C%22%3A%22Gpf_Rpc_Server%22%2C+%22M%22%3A%22run%22%2C+%22requests%22%3A%5B%7B%22C%22%3A%22Pap_Merchants_Transaction_TransactionsGrid%22%2C+%22M%22%3A%22getRows%22%2C+%22sort_col%22%3A%22dateinserted%22%2C+%22sort_asc%22%3Afalse%2C+%22offset%22%3A'+str(i)+'%2C+%22limit%22%3A'+str(i+500)+'%2C+%22filters%22%3A%5B%5B%22rstatus%22%2C%22IN%22%2C%22A%2CP%22%5D%2C%5B%22rtype%22%2C%22IN%22%2C%22C%2CS%22%5D%5D%2C+%22columns%22%3A%5B%5B%22id%22%5D%2C%5B%22id%22%5D%2C%5B%22commission%22%5D%2C%5B%22bannerid%22%5D%2C%5B%22name%22%5D%2C%5B%22rtype%22%5D%2C%5B%22tier%22%5D%2C%5B%22commissionTypeName%22%5D%2C%5B%22rstatus%22%5D%2C%5B%22userid%22%5D%5D%7D%5D%2C+%22S%22%3A%22'+session+'%22%7D'
        r=requests.get(url)
        df=pd.DataFrame(r.json())
        df=pd.DataFrame.from_dict(dict(df["rows"]))
        df=pd.DataFrame(columns=list(df[0][0]),data=list(list(df[0][1:])))
        final=pd.concat([df,final],ignore_index=True)
        final=final.drop([ 'commissionTypeName','tier'], axis=1)

        i+=500
    final.commission=final.commission.astype(float)
    final.to_csv("recommender_system/all_commissions.csv",index=False)


# In[9]:


get_all_commisions(login,password)


# ## Categories

# In[41]:


def get_all_categories(login,password):
    session=get_session_id(login,password)
    r = requests.get(
        'https://influencer.boostiny.app/scripts/server.php?D=%7B%22C%22%3A%22Gpf_Rpc_Server%22%2C%22M%22%3A%22run%22%2C%22requests%22%3A%5B%7B%22C%22%3A%22Pap_Features_BannersCategories_BannerCategoriesFilterGrid%22%2C%22M%22%3A%22getRows%22%2C%22offset%22%3A0%2C%22limit%22%3A100%7D%5D%2C%22S%22%3A%22'+session+'%22%7D')
    df=pd.DataFrame(r.json())
    limit=str(df["count"][0])
    i=0
    df=pd.DataFrame.from_dict(dict(df["rows"]))
    final=pd.DataFrame(columns=list(df[0][0]))
    while i<int(limit):
        url='https://influencer.boostiny.app/scripts/server.php?D=%7B%22C%22%3A%22Gpf_Rpc_Server%22%2C%22M%22%3A%22run%22%2C%22requests%22%3A%5B%7B%22C%22%3A%22Pap_Features_BannersCategories_BannerCategoriesFilterGrid%22%2C%22M%22%3A%22getRows%22%2C%22offset%22%3A'+str(i)+'%2C%22limit%22%3A'+str(i+500)+'%7D%5D%2C%22S%22%3A%22'+session+'%22%7D'
        r=requests.get(url)
        df=pd.DataFrame(r.json())
        df=pd.DataFrame.from_dict(dict(df["rows"]))
        df=pd.DataFrame(columns=list(df[0][0]),data=list(list(df[0][1:])))
        final=pd.concat([df,final],ignore_index=True)
        i+=500
    final.to_csv("recommender_system/categories.csv",index=False)


# In[42]:


get_all_categories(login,password)


# In[43]:


def get_all_banners_by_category(session,category):
    try:
        r = requests.get(
        'https://influencer.boostiny.app/scripts/server.php?D=%7B%22C%22%3A%22Gpf_Rpc_Server%22%2C+%22M%22%3A%22run%22%2C+%22requests%22%3A%5B%7B%22C%22%3A%22Pap_Merchants_Banner_BannersStatsGrid%22%2C+%22M%22%3A%22getRows%22%2C+%22sort_col%22%3A%22rorder%22%2C+%22sort_asc%22%3Atrue%2C+%22offset%22%3A0%2C+%22limit%22%3A30%2C+%22filters%22%3A%5B%5B%22rstatus%22%2C%22NE%22%2C%22Y%22%5D%2C%5B%22transactionstatus%22%2C%22IN%22%2C%22A%22%5D%2C%5B%22categoryid%22%2C%22IN%22%2C%22'+category+'%22%5D%5D%2C+%22columns%22%3A%5B%5B%22id%22%5D%2C%5B%22id%22%5D%2C%5B%22banner%22%5D%2C%5B%22campaignname%22%5D%2C%5B%22account%22%5D%2C%5B%22description%22%5D%2C%5B%22dateinserted%22%5D%5D%7D%5D%2C+%22S%22%3A%22'+session+'%22%7D'
        )
        df=pd.DataFrame(r.json())
        limit=str(df["count"][0])
        i=0
        df=pd.DataFrame.from_dict(dict(df["rows"]))
        final=pd.DataFrame(columns=list(df[0][0]))
        while i<int(limit):
            url='https://influencer.boostiny.app/scripts/server.php?D=%7B%22C%22%3A%22Gpf_Rpc_Server%22%2C+%22M%22%3A%22run%22%2C+%22requests%22%3A%5B%7B%22C%22%3A%22Pap_Merchants_Banner_BannersStatsGrid%22%2C+%22M%22%3A%22getRows%22%2C+%22sort_col%22%3A%22rorder%22%2C+%22sort_asc%22%3Atrue%2C+%22offset%22%3A'+str(i)+'%2C+%22limit%22%3A'+str(i+500)+'%2C+%22filters%22%3A%5B%5B%22rstatus%22%2C%22NE%22%2C%22Y%22%5D%2C%5B%22transactionstatus%22%2C%22IN%22%2C%22A%22%5D%2C%5B%22categoryid%22%2C%22IN%22%2C%22'+category+'%22%5D%5D%2C+%22columns%22%3A%5B%5B%22id%22%5D%2C%5B%22id%22%5D%2C%5B%22banner%22%5D%2C%5B%22campaignname%22%5D%2C%5B%22account%22%5D%2C%5B%22description%22%5D%2C%5B%22dateinserted%22%5D%5D%7D%5D%2C+%22S%22%3A%22'+session+'%22%7D'
            r=requests.get(url)
            df=pd.DataFrame(r.json())
            df=pd.DataFrame.from_dict(dict(df["rows"]))
            df=pd.DataFrame(columns=list(df[0][0]),data=list(list(df[0][1:])))
            final=pd.concat([df,final],ignore_index=True)
            final=final.drop(['isconfirmed','name','rtype'], axis=1)
            final=final.loc[final.rstatus.isin(["A"])]
            i+=500
        return final
    except:
        return "ERROR"


# In[44]:


def get_banners(login,password):
    session=get_session_id(login,password)
    categories=pd.read_csv("recommender_system/categories.csv").id
    cols=['id', 'campaignname', 'rstatus', 'banner', 'dateinserted',
       'description', 'account','category']
    final=pd.DataFrame(columns=cols)
    for cat in categories:
        df=get_all_banners_by_category(session,str(cat))
        if isinstance(df,str):
            continue
        df["category"]=cat
        final=pd.concat([df,final],ignore_index=True,sort=False)
    #final=final.drop(['isconfirmed','name','rtype'], axis=1)
    #Regroupement par categorie
    #plusieurs banniéres référencées avec plusieurs catégories
    final=final.groupby(by=['id', 'campaignname', 'rstatus', 'banner', 'dateinserted'
                    , 'description', 'account']).agg({'category':lambda x: list(x)}).reset_index()
    final.to_csv("recommender_system/banners.csv",index=False)


# In[45]:


get_banners(login,password)


# In[ ]:




