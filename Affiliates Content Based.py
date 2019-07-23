#!/usr/bin/env python
# coding: utf-8

# ## Recommender system that returns the most lucrative banners of a user's similar users (will be used as notifications)

# In[3]:


import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder as le
import datetime as dt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer


# ### Chargement des fichiers necessaires

# In[2]:


def import_data():
    affiliates=pd.read_csv("affiliates.csv")
    commissions=pd.read_csv("all_commissions.csv")
    banners=pd.read_csv("banners.csv")
    categories=pd.read_csv("categories.csv")
    affiliates.rename(columns={"data9":"categories","data4":"city","data10":"birth_date","data11":"gender"},inplace=True)
    affiliates.drop(columns=[x for x in affiliates.columns if x not in ["id","categories","city","birth_date","gender"]],inplace=True)
    affiliates=affiliates.astype({"city":"str","categories":"str","gender":"str"})
    return affiliates,commissions,banners,categories
#affiliates=pd.read_csv("Affiliates.csv",index_col=0)
#commissions=pd.read_csv("commissions.csv",index_col=0)
#banners=pd.read_csv("banners.csv",index_col=0)
#categories=pd.read_csv("categories.csv",index_col=0)


# #### Extraction of categories' ids from category_names

# In[4]:


def replace_cat_names_with_ids(affiliates,categories,end):
    #some of the first affiliates have category names instead of ids so but it was corrected for the new ones in the
    #the last update, end is usable when we know exactly after which row number the the update has begun 
    for idx,row in affiliates.iterrows():
        if idx<=end:
            if len(row["categories"])!=0:
                l_cat=row["categories"].split(";")
                ids=[]
                for i in range(1,len(l_cat)):
                    if l_cat[i].isdigit():
                        l_cat[i]=int(l_cat[i])
                    if isinstance(l_cat[i],str):
                        cat_id=categories.loc[(categories.name==l_cat[i]) ,"id"] #for those who have a list of category names
                    if isinstance(l_cat[i],int): #for those who have a list of category ids
                        cat_id=categories.loc[(categories.id==l_cat[i]) ,"id"]
                    if len(cat_id.values)>0:
                        cat_id=cat_id.values[0]
                        if(~np.isnan(int(cat_id))):
                            ids.append(cat_id)
                affiliates.loc[idx,"categories"]=ids
            else:
                affiliates.loc[idx,"categories"]=[]
    mlb = MultiLabelBinarizer()
    return pd.concat((affiliates.drop(columns=["categories"]),pd.DataFrame(mlb.fit_transform(affiliates.categories),columns="cat_"+mlb.classes_, index=affiliates.index))
                     ,axis=1)


# In[5]:


def data_preprocessing(affiliates,categories):
    affiliates=replace_cat_names_with_ids(affiliates=affiliates,categories=categories,end=affiliates.shape[0])
    #label encoding for affiliates
    affiliates.loc[~affiliates.gender.isin(["Male","Female"]),"gender"]="Missing"
    l_encoder=le()
    affiliates.gender=l_encoder.fit_transform(affiliates.gender,)
    #we will be working on the birth year of each user, no need for the whole date
    affiliates.loc[affiliates.birth_date=="null","birth_date"]=""
    affiliates.birth_date=pd.to_datetime(affiliates.birth_date)
    affiliates.birth_date=affiliates.birth_date.dt.year
    affiliates.birth_date.fillna(0,inplace=True)
    #dummies generation for city
    affiliates=pd.concat([affiliates,pd.get_dummies(affiliates.city)],axis=1)
    affiliates.drop(axis=0,columns=["city"],inplace=True)
    return affiliates


# In[6]:


def get_cos_sim_matrix(df):
    return cosine_similarity(df,df)


# In[7]:


def get_similar_users(id_,threshold,affiliates):
    cosine_sim=get_cos_sim_matrix(affiliates.drop(columns=["id"]))
    indices = pd.Series(affiliates.index, index=affiliates.id).drop_duplicates()
    idx = indices[id_]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [x for x in sim_scores if x[1]>threshold]
    sim_scores=sim_scores[1:]
    aff_indices = [i[0] for i in sim_scores]
    return affiliates.iloc[aff_indices,:],sim_scores


# In[20]:


def get_best_banners_from_similar_users(id_,threshold,banners_number):
    affiliates,commissions,banners,categories=import_data()
    affiliates=data_preprocessing(affiliates=affiliates,categories=categories)
    a,s=get_similar_users(id_,threshold,affiliates)
    commissions=commissions.groupby(["userid","bannerid"]).agg({"commission":sum}).reset_index()
    res=commissions.loc[commissions.userid.isin(a.id),:].groupby("bannerid").agg({"commission":sum}).reset_index().sort_values(by="commission",ascending=False)
    return res.loc[res.bannerid.isin(banners.id),:][:banners_number]


# ### Test

# In[1]:


#get_best_banners_from_similar_users(id_="8903",threshold=0.9,banners_number=10)

