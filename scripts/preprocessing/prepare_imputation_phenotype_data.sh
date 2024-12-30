#!/usr/bin/env bash

# Replace x filling (convention for missing values in GN) by 0 for imputation to take place later

less ../../processed_data/project_trimmed_phenotype_file.bimbam | sed 's/x/0/g' | less > ../../processed_data/project_prepared_phenotype_file.bimbam
