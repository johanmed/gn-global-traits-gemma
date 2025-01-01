#!/usr/bin/env python

# Script 7

# Impute missing values in project_prepared_phenotype_data.bimbam


import pandas as pd
import numpy as np

trimmed_BXD_data=pd.read_csv('../../processed_data/project_fully_trimmed_phenotype_file.bimbam', header=None)
trimmed_data=trimmed_BXD_data.copy()

#print('trimmed data looks like \n', trimmed_data.head())

f1=open('../../processed_data/order_trait_names_phenotype_file.csv', 'r')
order_trait_names=f1.readline().split(',') # get an array of the trait names in the same order as the phenotype file used
#print('List of trait names is: ', order_trait_names)
#print(f'List of trait names has {len(order_trait_names)} elements')
f1.close()


from sklearn.impute import KNNImputer

def impute_missing_column(column_data):
    imputer=KNNImputer() 
    return imputer.fit_transform(column_data)

    

def impute_missing_dataset(dataset, order_traits):
    new_dataset={}
    new_order_traits=[]
    for col in dataset.columns:
        #print(f'the index is {ind} and the column name {col}')
        data=dataset[col]
        if data.notna().any(): # only take columns with data for imputation 
            imputed_col=impute_missing_column(pd.DataFrame(data))
            #print('imputed col is \n', imputed_col)
            new_col=[i[0] for i in imputed_col]
            #print('new col is \n', new_col)
            
            new_dataset[col]=new_col
            new_order_traits.append(order_traits[col])
        
    imputed_dataset=pd.DataFrame(new_dataset)
    
    return imputed_dataset, new_order_traits

imputed_BXD_data, order_traits=impute_missing_dataset(trimmed_data, order_trait_names)
#print('Imputed data is \n', imputed_BXD_data.head())
#print('New order trait names is: ', order_traits)
#print('Number of traits kept after modification', len(order_traits))

imputed_BXD_data.to_csv("../../processed_data/project_imputed_phenotype_file.bimbam", index=False, header=False)


# Save the new order of the trait names
f2=open('../../processed_data/modified_order_trait_names_phenotype_file.csv', 'w')
f2.write(','.join(order_traits))
f2.close()
