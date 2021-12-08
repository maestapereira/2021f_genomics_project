#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# In[6]:


url_data = 'https://github.com/alura-cursos/imersaodados3/blob/main/dados/dados_experimentos.zip?raw=true'

df_raw = pd.read_csv(url_data, compression = 'zip')

df_raw.head()


# In[10]:


df_raw.columns[:4]


# In[19]:


df_english = df_english.rename(columns={'tratamento':'drug', 'tempo':'time', 'dose':'dosage', 'droga':'drug'})


# In[20]:


df_english.drug[df_english.drug=='com_droga'] = True


# In[21]:


df_english.drug[df_english.drug!='com_droga'] = False


# In[22]:


df_english.head()


# In[23]:


import os


# In[27]:


os.chdir('genomics_project\\genomics_project')
os.getcwd()


# In[28]:


df_english.to_csv('raw_data.zip', compression='zip')


# In[ ]:




