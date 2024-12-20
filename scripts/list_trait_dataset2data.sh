#!/usr/bin/env bash

for i in {1..5661}; do
	dataset_id=$(cut -d, -f1 ../processed_data/list_dataset_name_trait_id.csv | tail -n +3 | head -n $i | tail -n 1)
	trait_id=$(cut -d, -f2 ../processed_data/list_dataset_name_trait_id.csv | tail -n +3 | head -n $i | tail -n 1)
	curl https://genenetwork.org/api/v_pre1/sample_data/${dataset_id}/${trait_id} > ../processed_data/phenotype_file_${trait_id}_${dataset_id}.json
done

