# Recommender-System

This Recommender System was developped with another teammate for a marketing start-up named Boostiny dedicated for nano influencers. Its
main objective is to help the apps users find the products that fit them the most.

All python requirements can be found in requirements.txt

Boostiny has a Post Affiliate Pro account to store their users' data. Data loading code can be found in Boostiny.ipynb. We are using the 
python 'requests' library to load it since PAP (Post Affiliate Pro) is using http requests.

We have chosen to develop an hybrid recommender system since Boostiny doesn't have a large amount of data and also due to its robustness ("BannersHybrid.ipynb")&nbsp;
  For the content based RS, we have chosen to mainly work with Cosinus Similarity and Euclidian Distances ("AffiliatesContentBased.ipynb","BannersContentBased.ipynb")&nbsp;
  For the collaborative one, we used deep learning approaches (Light FM,Word Embedding) ("CollaborativeRecommenderSystem.ipynb")&nbsp;
  
The Recommender System was deployed with Flask on an AWS Server (Deployement.ipynb)
