#!/usr/bin/env python

import pandas as pd

# Apply series of modifications to project_phenotype_file.bimbam to make it contain the same lines as project_genotype_file.bimbam


# 1. Handle reading of files

f=open('../../processed_data/project_phenotype_file.bimbam')

read_lines=f.readlines()

longest_line=''
longest_length=0
for line in read_lines:
    if len(line)>longest_length:
        longest_length=len(line)
        longest_line=line
        
#print('Longest line: ', longest_line)

elements=longest_line.split(',')
#print('Elements: ', elements)

num_columns=len(elements)
#print('Number of columns: ', num_columns)

container={}

for x in read_lines:
    y=x.split(',')
    for z in y[1:]:
        if y[0] not in container.keys():
            container[y[0]]=[]
        else:
            container[y[0]].append(float(z))
    for rem in range(num_columns-len(y)):
        container[y[0]].append('x')

#print('Container: ', container)
    
ori_pheno=pd.DataFrame(container)
#print('Original phenotype: \n', ori_pheno.head())

ori_geno=pd.read_csv('../../processed_data/sample_BXD_genotype_file.csv', index_col=0)
#print('Original genotype: \n', ori_geno.head())


# 2. Remove lines in phenotype file not in genotype file

ori_pheno_transposed=ori_pheno.transpose(copy=True) # transpose dataframe to have lines on the rows
#print('Transposed phenotype file: \n', ori_pheno_transposed.head())


list_lines_pheno=ori_pheno_transposed.index # get labels
#print('Lines phenotype file: ', list_lines_pheno)

list_lines_geno=ori_geno.index # same
#print('Lines genotype file: ', list_lines_geno)

diff_to_remove=[]
for i in list_lines_pheno:
    if i not in list_lines_geno:
        diff_to_remove.append(i)
        
#print('Lines to remove: ', diff_to_remove) 

ori_pheno_transposed_trimmed=ori_pheno_transposed.drop(axis=0, labels=diff_to_remove) # remove lines not in genotype file
#print('Trimmed phenotype file: \n', ori_pheno_transposed_trimmed.head())




# 3. Add lines of genotype file missing in phenotype file

diff_to_add={}
for j in list_lines_geno:
    if j not in list_lines_pheno:
        diff_to_add[j]=['x' for rem in range(num_columns)]
#print('Lines to add: ', diff_to_add.keys())
        
lines_to_add=pd.DataFrame(diff_to_add)
lines_to_add_transposed=lines_to_add.transpose(copy=True)


total=pd.concat([ori_pheno_transposed_trimmed, lines_to_add_transposed]).iloc[:, :-1] # add new lines to phenotype data
#print('Complete phenotype file: \n', total.head())



# 4. Sort order of lines in phenotype file according to order in genotype file

final=pd.DataFrame()
for e, l in enumerate(list_lines_geno):
    #print('l is: ', l)
    final[l]=total.iloc[e, :] # need to select a specific row since lines are on rows
    
final_transposed=final.transpose(copy=True)
#print('Final transposed: \n', final_transposed.head())
final_transposed.to_csv('../../processed_data/project_trimmed_phenotype_file.bimbam', header=False, index=False) # save data in file
