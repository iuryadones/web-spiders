
# coding: utf-8

# In[1]:


import pymongo
from pymongo import MongoClient


# In[2]:


connection = MongoClient('localhost', 27018)
connection.database_names()


# In[3]:


database = connection['portal_transparencia']
database.collection_names()


# In[4]:


collection = database['dados_abertos']
collection.count()


# In[5]:


cursor = collection.find({})


# In[ ]:


for document in cursor:
    print(document)


# In[ ]:




