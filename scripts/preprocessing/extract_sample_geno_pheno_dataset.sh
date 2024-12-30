#!/usr/bin/env bash

# Get rqtl2 bundles of some datasets related to the project to compare genotype files to build a common genotype file and phenotype file

cd ../../processed_data/sample_rqtl2_geno_pheno_datasets # change directory to save easily zip files

for i in {1..4}; do # just get for the first 4 datasets and experiment on them
	dataset_id=$(cut -d, -f1 ../list_dataset_name_trait_id.csv | tail -n +3 | head -n $i | tail -n 1)
	curl -O https://genenetwork.org/api/v_pre1/genotypes/rqtl2/BXD/${dataset_id}.zip
	unzip ${dataset_id}.zip -d ${dataset_id}
	rm ${dataset_id}.zip 
done
