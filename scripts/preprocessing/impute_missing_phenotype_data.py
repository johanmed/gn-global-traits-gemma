#!/usr/bin/env python

# Script 7

# Impute missing values in project_prepared_phenotype_data.bimbam


import pandas as pd
import numpy as np

trimmed_BXD_data=pd.read_csv('../../processed_data/project_fully_trimmed_phenotype_file.bimbam', header=None)
trimmed_data=trimmed_BXD_data.copy()

#print('trimmed data looks like \n', trimmed_data[:5])

f1=open('../../processed_data/order_trait_names_phenotype_file.csv', 'r')
order_trait_names=f1.read().split(',') # get an array of the trait names in the same order as the phenotype file used
f1.close()

from sklearn.impute import KNNImputer

def impute_missing_column(column_data):
    imputer=KNNImputer(missing_values=0.0) 
    return imputer.fit_transform(column_data)

    

def impute_missing_dataset(dataset):
    new_data={}
    for (ind, col) in enumerate(dataset.columns):
        data=pd.DataFrame(dataset[col])
        #print('data is \n', data)
        imputed_col=impute_missing_column(data)
        if len(imputed_col)==0:
            del order_trait_names[ind]
            continue # ignore columns with no data for imputation (all values are 0)
        #print('imputed col is \n', imputed_col)
        new_col=[i[0] for i in imputed_col]
        #print('new col is \n', new_col)
        new_data[col]=new_col
    imputed_data=pd.DataFrame(new_data)
    return imputed_data

imputed_BXD_data=impute_missing_dataset(trimmed_data)
#print('imputed data is \n', imputed_BXD_data.head())

#imputed_BXD_data.to_csv("../../processed_data/project_imputed_phenotype_file.bimbam", index=False)

# Save the new order of the trait names
f2=open('../../processed_data/modified_order_trait_names_phenotype_file.csv', 'w')
f2.write(','.join(order_trait_names))
f2.close()
