# import libraries
import pandas as pd
import os

# raw data in portuguese
url_data = 'https://github.com/alura-cursos/imersaodados3/blob/main/dados/dados_experimentos.zip?raw=true'
# make data into df, decompressing it
df_feat = pd.read_csv(url_data, compression = 'zip')
# create df and traslate data columns
df_feat = df_feat.rename(columns={'tratamento':'with_drug', 'tempo':'time', 'dose':'dosage', 'droga':'drug'})
# make drug column into boolean, True is for drug, False if for control
df_feat.with_drug = df_feat.with_drug=='com_droga'
# cd where df will be saved
os.chdir('genomics_project\\genomics_project')
os.getcwd()
# save features in a zip file
df_feat.to_csv('feature_data.zip', compression='zip')

# save labels in a zip file
df_labels = pd.read_csv('https://github.com/alura-cursos/imersaodados3/blob/main/dados/dados_resultados.csv?raw=true')
df_labels.head()
df_labels.to_csv('label_data.zip', compression='zip')

# save features and labels in a single zip file
df_raw = pd.merge(df_feat, df_labels, on='id')
df_raw['n_moa'] = df_labels.drop('id', axis=1).sum(axis=1)
df_labels.to_csv('raw_data.zip', compression='zip')
