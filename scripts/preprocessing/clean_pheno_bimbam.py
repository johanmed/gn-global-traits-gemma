#!/usr/bin/env python

# Script 6b

import pandas as pd

"""
Apply series of modifications to project_phenotype_file.bimbam to make it contain the same lines as project_genotype_file.bimbam
"""

# 1. Handle reading of files

# 1.1. Reformat phenotype file

f=open('../../processed_data/project_phenotype_file.bimbam')

read_lines=f.readlines()

container={}

for x in read_lines:
    y=x.split(',')
    for z in y[1:]:
        u, v=z.split(':')
        container[(y[0], u)]=float(z)

row_names=[]
col_names=[]

for i in container.keys():
    a, b = i
    row_names.append(a)
    col_names.append(b)

ori_pheno=pd.DataFrame(np.full((236, 19542), 0.0), index=row_names, columns=col_names, ) # 236 lines and 19542 unique pairs of trait and dataset id

for i in container.keys():
    a, b= i
    ori_pheno.loc[a, b]=container[i]


#print('Phenotype data looks like: \n', ori_pheno.head())


# 1.2. Read genotype file

ori_geno=pd.read_csv('../../processed_data/sample_BXD_genotype_file.csv', index_col=0)

ori_geno_transposed=ori_geno.transpose(copy=True) # transpose dataframe to have lines on the rows

#print('Transposed genotype file: \n', ori_geno_transposed.head())




# 2. Remove lines in phenotype file not in genotype file



list_lines_pheno=ori_pheno.index # get labels
#print('Lines phenotype file: ', list_lines_pheno)

list_lines_geno=ori_geno_transposed.columns # same
#print('Lines genotype file: ', list_lines_geno)

diff_to_remove=[]
for i in list_lines_pheno:
    if i not in list_lines_geno:
        diff_to_remove.append(i)
        
#print('Lines to remove: ', diff_to_remove) 

ori_pheno_trimmed=ori_pheno.drop(axis=0, labels=diff_to_remove) # remove lines not in genotype file
#print('Trimmed phenotype file: \n', ori_pheno_trimmed.head())




# 3. Add lines of genotype file missing in phenotype file

diff_to_add={}
for j in list_lines_geno:
    if j not in list_lines_pheno:
        diff_to_add[j]=[0 for rem in range(19542)] # default number of phenotypes in file is 19542
#print('Lines to add: ', diff_to_add.keys())
        
lines_to_add=pd.DataFrame(diff_to_add)

total=pd.concat([ori_pheno_trimmed, lines_to_add]).iloc[:, :-1] # add new lines to phenotype data
#print('Complete phenotype file: \n', total.head())


# 4. Sort order of lines in phenotype file according to order in genotype file

final=pd.DataFrame()

for l in list_lines_geno:
    #print('l is: ', l)
    final[l]=total.loc[l, :] # need to select the row with the same line
    
final_transposed=final.transpose(copy=True) # need to transpose because lines on columns in dataframe final
#print('Final transposed: \n', final_transposed.head())

final_transposed.to_csv('../../processed_data/project_trimmed_phenotype_file.bimbam') # save traits and lines names with data

final_transposed.to_csv('../../processed_data/project_fully_trimmed_phenotype_file.bimbam', header=False, index=False) # save data without traits and lines names

order_trait_names= final_transposed.columns # extract order of trait names for future referencing

f=open('../../processed_data/order_trait_names_phenotype_file.csv', 'w')
f.write(','.join(order_trait_names))
f.close()


