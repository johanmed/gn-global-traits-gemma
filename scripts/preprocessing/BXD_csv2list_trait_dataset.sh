#!/usr/bin/env bash

# Extract only the lines of BXD_traits.csv containing comma separated values

tail -n +5 ../../raw_data/BXD_traits.csv | cut -d, -f 5,6 > ../../processed_data/list_dataset_name_trait_id.csv
