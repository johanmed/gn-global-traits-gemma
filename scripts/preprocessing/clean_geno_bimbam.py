#!/usr/bin/env python

# Script 6a

# Apply some series of modifications to transpose genotype file and format it as rows=markers and columns=lines as expected by gemma

import pandas as pd

ori_geno=pd.read_csv('../../processed_data/sample_BXD_genotype_file.csv') # read in data from appropriate file

transposed_geno=ori_geno.transpose(copy=True) # proceed to transposition
#print('transposed', transposed_geno.head())

transposed_geno_no_lines=transposed_geno.iloc[1:, :] # remove the row of RI lines
#print('transposed and transformed', transposed_geno_no_lines.head())

transposed_geno_no_lines.to_csv('../../processed_data/project_genotype_file.bimbam', header=False) # save dataframe
