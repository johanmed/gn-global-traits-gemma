#!/usr/bin/env python

# Process json phenotype files and create a single bimbam phenotype file where phenotype values of a given trait are added as a different column

import os
import re

list_json_files=[os.path.join('../processed_data', file) for file in os.listdir('../processed_data') if 'pheno' in file]


def process_json_bimbam(json_filename, bimbam_filename):
    """
    - Extract for a given json file, the strain names and the phenotype values
    - Add a new line with strain name and phenotype value if strain not yet in bimbam strain column
    - Add a new phenotype column when strain name already listed (strain names are not yet listed in the correct order as they are continuously modified)
    """
    
    json=open(json_filename)
    json_contents=json.readlines()
    json.close()
        
    container=[]
    
    for (x,y) in enumerate(json_contents):
    
        strain_found=re.search('sample_name_2', y)
        
        if not (strain_found==None):
            value_found=re.search('value', json_contents[x+1])
            
            strain_extract= "".join(char for char in strain_found.string[-10:-1] if char.isalnum())
            print('strain extract is ', strain_extract)
            
            value_extract="".join(char for char in value_found.string[-10:-1] if char.isdigit() or char=='.')
            print('value extract is ', value_extract)
            
            container.append([strain_extract, value_extract])
    
    print('container is ', container)
    
    bimbam1=open(bimbam_filename, 'a')
    
    bimbam2=open(bimbam_filename)
    bimbam2_contents=bimbam2.read()
    bimbam2.close()
    
    for a in container:
        bimbam1=open(bimbam_filename, 'a')
        if a[0] in bimbam2_contents:
            old_string=(re.search(f'{a[0]}.*\n', bimbam2_contents).group())[:-1]
            print('old string is ', old_string)
            new_string=bimbam2_contents.replace(old_string, f'{old_string}, {a[1]}')
            print('new string is ', new_string)
            
            bimbam1.write(f'{new_string}\n')
            
        bimbam1.write(f'{a[0]}, {a[1]}\n')
        bimbam1.close()
    

def contains_phenotype_data(json_filename):
    """
    Checks if a phenotype file contains phenotype data or not
    """
    
    f=open(json_filename)
    line1=f.readline()
    f.close()
    if line1.startswith('['):
        return True
    else:
        return False
        

f=open('../processed_data/project_phenotype_file.bimbam', 'a')
f.write(f'strain_id, trait_value\n') # add header for clarity
f.close()


for jsonf in list_json_files:
    print(f'Processing {jsonf}')
    if contains_phenotype_data(jsonf):
        print(f'File {jsonf} contains data and can go for actual processing')
        process_json_bimbam(jsonf, '../processed_data/project_phenotype_file.bimbam')
    

