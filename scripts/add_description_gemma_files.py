#!/usr/bin/env python

import pandas as pd
import os

gemma_files=[i for i in os.listdir('../data/') if 'assoc' in i and 'relevant' in i and 'new' not in i] # read files names from directory and store in array
gemma_files=sorted(gemma_files) # sort by names

info_read=open('../data/BXD_traits_selected_info.csv').readlines() # read contents of metadata file
info_read=sorted(info_read) # sort based on trait id

def add_desc_gemma_assoc(file, val1, val2):
        """
        Write to a new gemma file contents of old gemma file, val1 (trait category), val2(full description) tab separated
        """
        
        gemma_content=open(file).readlines()
        to_write=[]
        for u in gemma_content:
            to_write.append(f'{u.strip()}\t{val1}\t{val2}')
            
        ready_to_write='\n'.join(to_write)
        gemma_write=open(f'new_{file}', 'w')
        gemma_write.write(ready_to_write)
            
def process_file(info_read, gemma_files, add_desc_gemma_assoc):
    """
    Process all gemma files creating a new file for each using metadata information to infer category of trait and full trait description
    """
    for i, j in enumerate(info_read):
        x, y, z = j.split('\t')
        for f in gemma_files:
            o, p, q, r=f.split('_')
            l, m, n= r.split('.')
            if i==int(l[5:]) and y=='Diabetes trait':
                print(f'Inferred diabetes trait for {f}')
                add_desc_gemma_assoc(f, 0, z)
            elif i==int(l[5:]) and y=='Immune system trait':
                print(f'Inferred Immune system trait for {f}')
                add_desc_gemma_assoc(f, 1, z)
            elif i==int(l[5:]) and y=='Gut microbiome trait':
                print(f'Inferred Gut microbiome trait for {f}')
                add_desc_gemma_assoc(f, 2, z)

process_file(info_read, gemma_files, add_desc_gemma_assoc)
