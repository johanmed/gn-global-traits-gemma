#!/usr/bin/env bash

# Extract only the lines of the datasets files containing comma separated values

cd ../../raw_data/global_search_datasets/

for i in ./*
do
	tail -n +5 $i | cut -d, -f 5,6 > trimmed_$i
done
