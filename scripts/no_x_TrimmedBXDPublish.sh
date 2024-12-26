#!/usr/bin/env bash

less ../processed_data/TrimmedBXDPublish.csv | sed 's/x/0/g' | less > ../processed_data/no_x_TrimmedBXDPublish.csv
