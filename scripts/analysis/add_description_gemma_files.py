#!/usr/bin/env python

# Script 11

# Add trait category and full description to association not inplace, after gemma files transformation


import pandas as pd
import os

gemma_files=[os.path.join('../../output/association/', i) for i in os.listdir('../../output/association/') if ('assoc' in i) and ('relevant' in i) and ('new' not in i)] # read files names from directory and store in array
gemma_files=sorted(gemma_files) # sort by names where the index after assoc is used

info=open('../../processed_data/metadata_phenotype_info_file.json')
info_read=info.readlines() # read contents of metadata file
info.close()

metadata=[] # metadata of phenotypes added in the order of the phenotypes in the project_imputed_phenotype_file.bimbam offhand, so no need to sort

for line in info_read:
    description_found=re.search('description', line)
    if not (description_found==None):
        description_extract= "".join(char for char in description_found.string[15:] if char.isalnum())
        print('description extract is ', description_extract)
        metadata.append(description_extract)
    


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
            
def process_file(metadata, gemma_files, add_desc_gemma_assoc):
    """
    Process all gemma files creating a new file for each using metadata information to infer category of trait and full trait description
    """
    for i, j in enumerate(metadata):
        
        for f in gemma_files:
            o, p, q, r=f.split('_')
            l, m, n= r.split('.')
            if (i+1)==int(l[5:]) and ('diabetes' in j or 'diabet' in j): # might need to add more keywords related to diabetes
                print(f'Inferred diabetes trait for {f}')
                add_desc_gemma_assoc(f, 0, j)
            elif (i+1)==int(l[5:]) and 'immune' in j: # might need to add more keywords related to immune system
                print(f'Inferred Immune system trait for {f}')
                add_desc_gemma_assoc(f, 1, j)
            elif (i+1)==int(l[5:]) and ('gut' in j or 'gastro' in j): # might need to add more keywords related to gastrointestinal system
                print(f'Inferred Gut microbiome trait for {f}')
                add_desc_gemma_assoc(f, 2, j)

#process_file(info_read, gemma_files, add_desc_gemma_assoc)
