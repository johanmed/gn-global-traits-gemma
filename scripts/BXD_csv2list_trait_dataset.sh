#!/usr/bin/env bash

tail -n +5 ../raw_data/BXD_traits.csv | cut -d, -f 5,6 > ../processed_data/list_dataset_name_trait_id.csv
