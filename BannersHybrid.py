#!/usr/bin/env python
# coding: utf-8

# In[1]:


import import_ipynb
import RecommenderSystem as recommenderSystem
import BannersContentBased as bannersContentBased
import pandas as pd
import json


# In[2]:


def import_data():
    final=recommenderSystem.import_data()
    banners=bannersContentBased.import_data()
    collaborativeRecommendedBannersMatrix=recommenderSystem.create_banner_emdedding_distance_matrix(final=final)
    contentBasedRecommendedBannersMatrix=bannersContentBased.get_final_cos_sim_matrix(banners=banners)
    aux=pd.DataFrame(contentBasedRecommendedBannersMatrix)
    indices=bannersContentBased.get_indices(banners)
    aux.columns=indices.index
    aux.index=indices.index
    aux.drop(columns=aux.columns[~aux.columns.isin(collaborativeRecommendedBannersMatrix.columns)],inplace=True)
    aux.drop(index=aux.index[~aux.index.isin(collaborativeRecommendedBannersMatrix.index)],inplace=True)
    collaborativeRecommendedBannersMatrix=collaborativeRecommendedBannersMatrix.reindex(aux.columns,axis=1)
    collaborativeRecommendedBannersMatrix=collaborativeRecommendedBannersMatrix.reindex(aux.index,axis=0)
    #At this stage the two datasets have the same columns and indexes and are ordred the same way
    return collaborativeRecommendedBannersMatrix,aux


# In[35]:


def get_recommendations(threshold,id_):
    collaborative,content_based=import_data()
    cosine_sim=(collaborative+content_based)/2
    indices = pd.Series(content_based.index, index=content_based.index).drop_duplicates()
    idx = indices[id_]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [x for x in sim_scores if x[1]>threshold]
    sim_scores=sim_scores[1:]
    banner_indices = [i[0] for i in sim_scores]
    sims=[i[1] for i in sim_scores]
    idx=indices[banner_indices]
    dic={"banner_ids":list(idx),"sim_scores":sims}
    return dic


# In[36]:


#get_recommendations(0.4,'d8343bcd')


# In[ ]:




