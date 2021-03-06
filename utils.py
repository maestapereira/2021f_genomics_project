# -*- coding: utf-8 -*-
"""utils.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1O5K3rplWKh5IvYgqdBtW8tasJkm24NmI
"""

# Utils to read and convert data easily
# 12/15/2021

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from pathlib import Path

from sklearn.model_selection import StratifiedShuffleSplit

def read_data(path=Path("/gdrive/My Drive/columbia_masters/classes/2021_f/genomics/genomics_project")):
    """Loads feature, label, and raw data from .zip files

    Parameters
    ----------
    path : Path object
    Path where .zip files are.

    Returns
    -------
    df_feature : `pd.DataFrame`
        features pandas data frame
    df_labels : `pd.DataFrame`
        hot encoded labels pandas data frame
    df_raw : `pd.DataFrame`
        features and labels pandas data frame
    """
    # features pandas data frame
    df_feature = pd.read_csv(path / 'feature_data.zip', compression = 'zip').drop(columns=['Unnamed: 0'])
    # labels pandas data frame
    df_labels = pd.read_csv(path / 'label_data.zip', compression = 'zip').drop(columns=['Unnamed: 0'])
    # combined pandas data frame
    df_raw = pd.merge(df_feature, df_labels, on='id')
    
    return df_feature, df_labels, df_raw

def get_n_moa(df_labels):
    """Counts and plots histogram number of MOAs per row in labels pd.DataFrame

    Parameters
    ----------
    df_labels : `pd.DataFrame`
        hot encoded labels pandas data frame.

    Returns
    -------
    n_moa : `pd.Series`
        number of MOAs (labels) per row in hot encoded labels.
    """
    n_moa = df_labels.drop('id', axis=1).sum(axis=1)
    return n_moa

def get_plot_n_moa(df_labels):
    """Plots histogram number of MOAs per row in labels pd.DataFrame

    Parameters
    ----------
    df_labels : `pd.DataFrame`
        hot encoded labels pandas data frame.

    Returns
    -------
    n_moa : `pd.Series`
        number of MOAs (labels) per row in hot encoded labels.
    """
    n_moa = get_n_moa(df_labels)
    plt.hist(n_moa)
    plt.title = 'Number of occurences by number of moa'
    plt.xlabel('Number of moa')
    plt.ylabel('Number of occurences')

    plt.grid(True)
    plt.show()
    return n_moa

def sel_labels_by_occur(df_labels, df_raw, min_label_occur=100):
    """Drops labels (columns) that occur less than min_label_occur in df_labels 
    and df_raw pd.DataFrames.

    Parameters
    ----------
    df_labels : `pd.DataFrame`
        hot encoded labels pandas data frame
    df_raw : `pd.DataFrame`
        features and labels pandas data frame
    min_label_occur : `int`
        minimum number of occurences of a label for it to be included.
        Defaults to 100.

    Returns
    -------
    sel_labels : `pd.DataFrame`
        hot encoded labels pandas data frame without removed labels.
    sel_raw
        features and labels pandas data frame (without least occuring labels)
    """
    # number of occurences per label
    labels_count = df_labels.drop(columns='id').sum(axis=0)
    # columns to be dropped
    drop_labels = list(labels_count[(labels_count<min_label_occur)].index)

    sel_labels = df_labels.drop(columns=drop_labels)
    sel_raw = df_raw.drop(columns=drop_labels)

    return sel_labels, sel_raw

def get_n_moa_per_row(df_feature, df_labels, n_moa_per_row=1):
    """Returns feature, and label data keeping only rows with n MOAs per row

    Parameters
    ----------
    df_feature : `pd.DataFrame`
        features pandas data frame
    df_labels : `pd.DataFrame`
        hot encoded labels pandas data frame
    n_moa_per_row: `int`
        number of MOAs per row.
        Defaults to 1

    Returns
    -------
    df_feature : `pd.DataFrame`
        features pandas data frame
    df_labels : `pd.DataFrame`
        hot encoded labels pandas data frame
    """
    # keep only rows with n moas
    n_moa = get_n_moa(df_labels)
    n_moa_idx = np.where(n_moa!=n_moa_per_row)[0]
    n_moa_feature = df_feature.drop(index=n_moa_idx).reset_index(drop=True)
    n_moa_labels = df_labels.drop(index=n_moa_idx).reset_index(drop=True)
    
    return n_moa_feature, n_moa_labels

def get_gene_exp_features(df_feature, in_numpy=False):
    """Makes feature pd.DataFrame into numpy array with floats and ints only

    Parameters
    ----------
    df_feature : `pd.DataFrame`
        features pandas data frame
    in_numpy : `bool`
        if features should be returned in numpy, with integers and floats only 
        (True) or in pd.DataFrame (False)
        Defaults to False.

    Returns
    -------
    gene_feature : `np.ndarray`
        Gene expression features nd array
        
    Notes
    -----
    gene_feature only has id column if in_numpy is False.
    """
    gene_cols = [col for col in df_feature.columns if (col.startswith('g-')|col.startswith('id'))]
    gene_feature = df_feature[gene_cols]
    if in_numpy == True:
        if np.isin('id', df_feature.columns):
            gene_feature = gene_feature.drop(columns=['id'])
        if np.isin('dtype', df_feature.columns):
            gene_feature = gene_feature.drop(columns=['dtype'])
        gene_feature = gene_feature.to_numpy()
        
    return gene_feature

def get_test_train_val(df_feature, df_labels):
    """Returns feature and label data with additional column `dtype` with test, 
    train or val. Split is made using sklearn's StratifiedShuffleSplit

    Parameters
    ----------
    df_feature : `pd.DataFrame`
        features pandas data frame
    df_labels : `pd.DataFrame`
        hot encoded labels pandas data frame

    Returns
    -------
    df_feat : `pd.DataFrame`
        features pandas data frame with additional column `dtype`
    df_lab : `pd.DataFrame`
        hot encoded labels pandas data frame with additional column `dtype`
    """
    # get train set
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
    print(sss)
    # we want copies, not to modify original datafames
    df_feat = df_feature
    df_lab = df_labels
    df_feat['dtype'] = 'test'
    df_lab['dtype'] = 'test'
    for train_index, test_index in sss.split(df_feature.drop(columns=['id']), df_labels.drop(columns=['id'])):
        df_feat.iloc[train_index, -1] = 'train'
        df_lab.iloc[train_index, -1] = 'train'
        df_feat.iloc[test_index, -1] = 'test'
        df_lab.iloc[test_index, -1] = 'test'

    # get test and validation sets
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.7, random_state=42)
    print(sss)
    for val_index, test_index in sss.split(df_feature.drop(columns=['id'])[df_feature['dtype'] == 'test'], df_labels.drop(columns=['id'])[df_labels['dtype'] == 'test']):
        df_feat.iloc[val_index, -1] = 'val'
        df_lab.iloc[val_index, -1] = 'val'
        df_feat.iloc[test_index, -1] = 'test'
        df_lab.iloc[test_index, -1] = 'test'

    return df_feat, df_lab

def split_labels_train_test_val(df_labels):
    """Returns train, test and validation sets of labels, no longer hot encoded

    Parameters
    ----------
    df_labels : `pd.DataFrame`
        hot encoded labels pandas data frame

    Returns
    -------
    train_labels : 1D `np.array` 
        train labels (NOT hot encoded)
    test_labels : 1D `np.array`
        test labels (NOT hot encoded)
    val_labels: 1D`np.array`
        val labels (NOT hot encoded)
    """
    train_labels = df_labels[df_labels.iloc[:, -1] == 'train'].drop(columns=['id', 'dtype']).to_numpy()
    train_labels = np.argmax(train_labels, axis=1)

    test_labels = df_labels[df_labels.iloc[:, -1] == 'test'].drop(columns=['id', 'dtype']).to_numpy()
    test_labels = np.argmax(test_labels, axis=1)

    val_labels = df_labels[df_labels.iloc[:, -1] == 'val'].drop(columns=['id', 'dtype']).to_numpy()
    val_labels = np.argmax(val_labels, axis=1)

    return train_labels, test_labels, val_labels

def get_labels_ordinal(df_labels):
    """Returns train, test and validation sets of labels, no longer hot encoded

    Parameters
    ----------
    df_labels : `pd.DataFrame`
        hot encoded labels pandas data frame

    Returns
    -------
    ordinal_labels : 1D `np.array` 
        labels, in integers (NOT hot encoded)
    """ 
    if np.isin('id', df_labels.columns):
        df_labels = df_labels.drop(columns=['id'])
    if np.isin('dtype', df_labels.columns):
        df_labels = df_labels.drop(columns=['dtype'])
    ordinal_labels = np.argmax(df_labels.to_numpy(), axis=1)
    
    return ordinal_labels

def split_features_train_test_val(df_feature, in_numpy=False):
    """Returns train, test and validation sets of features

    Parameters
    ----------
    df_feature : `pd.DataFrame`
        features pandas data frame
    in_numpy : `bool`
        if features should be returned in numpy, with integers and floats only 
        (True) or in pd.DataFrame (False)
        Defaults to False.

    Returns
    -------
    train_features : 1D `np.array` 
        train features
    test_features : 1D `np.array`
        test features
    val_features: 1D `np.array`
        val features
    """
    train_features = df_feature[df_feature.iloc[:, -1] == 'train'].drop(columns=['id', 'dtype']).reset_index(drop=True)
    test_features = df_feature[df_feature.iloc[:, -1] == 'test'].drop(columns=['id', 'dtype']).reset_index(drop=True)
    val_features = df_feature[df_feature.iloc[:, -1] == 'val'].drop(columns=['id', 'dtype']).reset_index(drop=True)
    if in_numpy==True:
        train_features = _features_from_pd_to_np(train_features)
        test_features = _features_from_pd_to_np(test_features)
        val_features = _features_from_pd_to_np(val_features)

    return train_features, test_features, val_features

def _features_from_pd_to_np(df_feature):
    """Makes feature pd.DataFrame into numpy array with floats and ints only

    Parameters
    ----------
    df_feature : `pd.DataFrame`
        features pandas data frame

    Returns
    -------
    np_feature : `np.ndarray`
        features nd array
    """
    temp = pd.get_dummies(df_feature)
    drug_cols = [col for col in temp.columns if col.startswith('drug_')]
    drug_int = (temp[drug_cols].idxmax(axis=0))-min(temp[drug_cols].idxmax(axis=0))
    df_feature['drug'] = drug_int.reset_index(drop=True).astype(int)
    df_feature.loc[np.where(df_feature.dosage=='D1')[0], 'dosage']=0
    df_feature.loc[np.where(df_feature.dosage=='D2')[0], 'dosage']=1
    df_feature['with_drug'] = df_feature['with_drug'].astype(int)
    return df_feature.to_numpy()
