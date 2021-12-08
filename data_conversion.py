#!/usr/bin/env python
# coding: utf-8

# import libraries
import pandas as pd
import os

# raw data in portuguese
url_data = 'https://github.com/alura-cursos/imersaodados3/blob/main/dados/dados_experimentos.zip?raw=true'
# make data into df, decompressing it
df_raw = pd.read_csv(url_data, compression = 'zip')

# create df and traslate data columns
df_english = df_english.rename(columns={'tratamento':'drug', 'tempo':'time', 'dose':'dosage', 'droga':'drug'})
# make drug column into boolean
df_english.drug[df_english.drug=='com_droga'] = True
df_english.drug[df_english.drug!='com_droga'] = False

# cd where df will be saved
os.chdir('genomics_project\\genomics_project')
os.getcwd()

# save df
df_english.to_csv('raw_data.zip', compression='zip')
