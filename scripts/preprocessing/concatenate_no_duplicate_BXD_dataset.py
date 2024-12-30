#!/usr/bin/env python

# Remove duplicates from raw and concatenate dataset files into a single file, after making the file contents 100% comma separated

import os
import pandas as pd

list_csv_files=[os.path.join('../../raw_data/global_search_datasets', file) for file in os.listdir('../../raw_data/global_search_datasets') if 'trimmed' in file]

container={}

for csv in list_csv_files:
    csv_data=pd.read_csv(csv, header=0, names=['dataset_id', 'trait_id'])
    for col in csv_data.columns:
        if col not in container.keys():
            container[col]=set()
        else:
            for el in list(csv_data.col):
                container[col].add(el)
            
new_container=pd.DataFrame(container)

new_container.to_csv('../../processed_data/list_dataset_name_trait_id.csv', header=False, index=False)


