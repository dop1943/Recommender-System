#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from flask import *
import json
import BannersContentBased as bannersContentBased
import BannersHybrid as bannersHybrid
import AffiliatesContentBased as affiliatesContentBased
import RecommenderSystem as recommenderSystem


# In[2]:


app = Flask(__name__)

@app.route('/test')
def test():
    return "We did it"

@app.route('/hybrid_recommendation')
def get_hybrid_banners_recommendation():
    id_ = request.args.get('id', None)
    if id_ is None:
        abort(404)
    else:
        dic=bannersHybrid.get_recommendations(0.2,id_)
        return json.dumps(dic)

@app.route('/banner_affiliate_recommendation')
def get_banner_affiliates_recommendations():
    id_ = request.args.get('id', None)
    if id_ is None:
        abort(404)
    else:
        res=affiliatesContentBased.get_best_banners_from_similar_users(id_,0.9,10)
        dic={"bannerid":list(res["bannerid"]),"commission":list(res["commission"])}
        return json.dumps(dic)

@app.route('/banner_banner_collab')
def banner_banner_List():
    id_ = request.args.get('id', None)
    if id_ is None:
        abort(404)
    else:
        b=recommenderSystem.banner_banner_recommendation(id_, n_banners = 10, show = False)
        dic={"banner_ids": b}
        return json.dumps(dic)
    

@app.route('/banner_banner_content')
def banner_banner_content():
    id_ = request.args.get('id', None)
    if id_ is None:
        abort(404)
    else:
        idx,sim=bannersContentBased.get_recommendations(id_)
        dic={"banner_ids":list(idx),"sim_scores":[i[1] for i in sim]}
        return json.dumps(dic)

@app.route('/banner_to_user')
def rec_list():
    id_ = request.args.get('id', None)
    if id_ is None:
        abort(404)
    else:
        rec_list = recommenderSystem.sample_recommendation_user(id_,5)
        dic={"banner_ids": rec_list}
        return json.dumps(dic)

@app.route('/user_to_banner')
def user_list():
    id_ = request.args.get('id', None)
    if id_ is None:
        abort(404)
    else:
        user_list = recommenderSystem.sample_recommendation_user_to_item(id_,10)
        dic={"user_ids": user_list}
        return json.dumps(dic)


# In[ ]:




