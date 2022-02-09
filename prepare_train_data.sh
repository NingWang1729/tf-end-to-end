#!/bin/bash

rm -rf Train_Sheets
mkdir Train_Sheets
mkdir Train_Sheets/images
mkdir Train_Sheets/labels
mkdir Train_Sheets/images/train
mkdir Train_Sheets/labels/train
python3 parse_annotations.py --generate_sheet_music_samples
tar -czvf train_data.tgz Train_Sheets
