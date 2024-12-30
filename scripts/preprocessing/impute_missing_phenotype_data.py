#!/usr/bin/env python

# Impute missing values in project_prepared_phenotype_data.bimbam


import pandas as pd
import numpy as np

trimmed_BXD_data=pd.read_csv('../../processed_data/project_prepared_phenotype_data.bimbam')
trimmed_data=trimmed_BXD_data.copy()

print(trimmed_data[:5])

from sklearn.impute import KNNImputer

def impute_missing_column(column_data):
    imputer=KNNImputer(missing_values=0)
    imputer.fit(column_data)
    new_data=imputer.transform(column_data)
    return new_data
    

def impute_missing_dataset(dataset):
    imputed_data=pd.DataFrame()
    imputed_data['id']=dataset.iloc[:, 0]
    for col in dataset.columns[1:]:
        new_col=impute_missing_column(np.array(dataset[col]).reshape(-1, 1))
        print(dataset[col])
        print(new_col)
        imputed_data[col]=pd.DataFrame(new_col)
    return imputed_data

imputed_BXD_data=impute_missing_dataset(trimmed_data)
imputed_BXD_data.to_csv("../../processed_data/project_imputed_phenotype_file.bimbam", index=False)

