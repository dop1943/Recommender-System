#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize as wt
import spacy
import re
nlp = spacy.load('fr_core_news_sm')
import json


# In[2]:


def import_data():
    banners=pd.read_csv("banners.csv")
    #Tranformation de la colonne catégorie en String pour faciliter les étapes à suivre
    for idx,row in banners.iterrows():
        s=row["category"].replace("["," ")
        s=s.replace("]"," ")
        s=s.replace(","," ")
        banners.iloc[idx,7]=s
    return banners


# In[3]:


#fonction permettant de degager les synonymes de chaque mot en français
def synonymes(l_mot):
    dic={}
    for mot in l_mot:
        syns=wn.synsets(mot,lang="fra")
        for i in range (0,len(syns)):
            mots=syns[i].lemma_names("fra")
            for m in mots:
                if m not in dic:
                    dic[m]=1
    return dic


# In[4]:


#fonction permettant de d'eliminer tout caractere autre que des lettres et les stopwords
def filter_non_alpha_text(text):
    stopWords=stopwords.words('french')
    filtred=[]
    text=str(text).lower()
    tokenized=wt(text)
    for w in tokenized:
        w = w.strip('\'"?,.')
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9].*$", w)
        if(w not in stopWords and val is not None):
            w=nlp(w)
            for token in w:
                w=token.lemma_#retrouver la forme primaire des mots, ex: arrivé--> arriver,jeux-->jeu
            filtred.append(w)
    return filtred


# In[5]:


#fonction permettant de creer une nouvelle colonne qui reunit campaign_name et banner avec du text cleaning 
#et generation de synonymes
def cb_creation(df):
    df["cb"]=""
    for idx,row in df.iterrows():
        final=row["campaignname"]+' '+row["banner"]
        final=filter_non_alpha_text(final)
        dic=synonymes(l_mot=final)
        final=list(dic.keys())
        separator=' '
        df["cb"][idx]=separator.join(final)
        if len(df["cb"][idx])==0:
            df["cb"][idx]=row["campaignname"]+' '+row["banner"]
    return df


# In[6]:


#fonction qui retourne la cos sim matrix
def get_cos_sim_matrix(col):
    col.astype(str)
    tfidf = TfidfVectorizer()
    #col = col.fillna('')
    tfidf_matrix_meta = tfidf.fit_transform(col)
    #linear kernek car on a deja calculé tf idf=> du linear kern nous donnera directement les valeur de cos sim.
    #==> juste pour accelerer les calculs
    return linear_kernel(tfidf_matrix_meta, tfidf_matrix_meta)


# In[7]:


def get_final_cos_sim_matrix(banners):
    banners=cb_creation(banners)
    cosine_sim_meta=get_cos_sim_matrix(banners["cb"])
    cosine_sim_cat=get_cos_sim_matrix(banners["category"])
    #cos sim des categories prend un poid de 1.5 par rapport à meta(peut etre ajusté)
    cosine_sim=(1.5*cosine_sim_cat+cosine_sim_meta)/2.5
    return cosine_sim


# In[8]:


def get_indices(banners):
    return pd.Series(banners.index, index=banners.id).drop_duplicates()


# In[9]:


def get_recommendations(id_):
    banners=import_data()
    cosine_sim=get_final_cos_sim_matrix(banners)
    indices = pd.Series(banners.index, index=banners.id).drop_duplicates()
    idx = indices[id_]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [x for x in sim_scores if x[1]>0.2]
    sim_scores=sim_scores[1:]
    banner_indices = [i[0] for i in sim_scores]
    return banners.iloc[banner_indices,:].id,sim_scores

