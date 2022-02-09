#!/bin/env python3

import re
import argparse
import json
import numpy as np
from PIL import Image

from image_cropper import crop_image
from generate_sheet_music import generate_five_staff_sheet, generate_six_staff_sheet

def crop_staffs():
    # Open file
    with open('./Grand_Staff_Sections_Train.json', 'r') as file:
        annotations = json.load(file)

    # Retrieve Pages
    annotations = annotations['annotations']['image']

    # Retrieve Train
    annotations = annotations[12:]

    # Separate into 5 and 6 staffs per page
    five_staffs = []
    six_staffs = []
    for page in annotations:
        if len(page['box']) == 5:
            five_staffs.append(page)
        elif len(page['box']) == 6:
            six_staffs.append(page)

    # Parse JSON for 5 staffs
    for page in range(len(five_staffs)):
        raw = five_staffs[page]
        temp = {'file' : raw['_name'], 'crops' : []}
        for crop in raw['box']:
            temp['crops'].append([int(float(crop['_xtl'])), int(float(crop['_ytl'])), int(float(crop['_xbr'])), int(float(crop['_ybr']))])
        five_staffs[page] = temp

    # Parse JSON for 6 staffs
    for page in range(len(six_staffs)):
        raw = six_staffs[page]
        temp = {'file' : raw['_name'], 'crops' : []}
        for crop in raw['box']:
            temp['crops'].append([int(float(crop['_xtl'])), int(float(crop['_ytl'])), int(float(crop['_xbr'])), int(float(crop['_ybr']))])
        six_staffs[page] = temp
    
    index = 0
    for staff in five_staffs:
        for crop in staff['crops']:
            crop_image(file=f"./Bach_Inventions/{staff['file']}", coords=crop, output=f"./Crops/five_{index}.png", dry=False)
            index += 1

    index = 0
    for staff in six_staffs:
        for crop in staff['crops']:
            crop_image(file=f"./Bach_Inventions/{staff['file']}", coords=crop, output=f"./Crops/six_{index}.png", dry=False)
            index += 1


def generate_sheet_music_samples(five_staff_sheets=1000, six_staff_sheets=1000):
    # Open file
    with open('./Grand_Staff_Crop_Labels_Train.json', 'r') as file:
        annotations = json.load(file)

    # Retrieve Pages
    annotations = annotations['annotations']['image']

    # Separate into 5 and 6 staffs per page
    five_staffs = []
    six_staffs = []
    for page in annotations:
        if re.search('five', page['_name']):
            five_staffs.append(page)
        elif re.search('six', page['_name']):
            six_staffs.append(page)

    # Parse JSON for 5 staffs
    for page in range(len(five_staffs)):
        raw = five_staffs[page]
        temp = {}
        temp['file'] = raw['_name']
        temp['id'] = re.search('\d+', raw['_name']).group()
        temp['coords'] = [int(float(raw['box']['_xtl'])), int(float(raw['box']['_ytl'])), int(float(raw['box']['_xbr'])), int(float(raw['box']['_ybr']))]
        five_staffs[page] = temp

    # Parse JSON for 6 staffs
    for page in range(len(six_staffs)):
        raw = six_staffs[page]
        temp = {}
        temp['file'] = raw['_name']
        temp['id'] = re.search('\d+', raw['_name']).group()
        temp['coords'] = [int(float(raw['box']['_xtl'])), int(float(raw['box']['_ytl'])), int(float(raw['box']['_xbr'])), int(float(raw['box']['_ybr']))]
        six_staffs[page] = temp

    # Sort by id
    five_staffs.sort(key=lambda x : int(x['id']))
    six_staffs.sort(key=lambda x : int(x['id']))

    # Generate 5 staff train data
    for index in range(five_staff_sheets):
        # Generate indices
        crop_indices = np.random.randint(35, size=5)
        image_file_name = f'./Train_Sheets/images/train/five_sheet_{index}'
        label_file_name = f'./Train_Sheets/labels/train/five_sheet_{index}'
        # Save annotations
        with open(f'{label_file_name}.txt', 'w') as file:
            for _ in range(5):
                fou = five_staffs[crop_indices[_]]
                # file.write(f"0, {22 + fou['coords'][0]}, {95 + fou['coords'][1] + _ * 420}, {22 + fou['coords'][2]}, {95 + fou['coords'][3] + _ * 420}\n")
                _xtl = 22 + fou['coords'][0]
                _ytl = 95 + fou['coords'][1] + _ * 420
                _xbr = 22 + fou['coords'][2]
                _ybr = 95 + fou['coords'][3] + _ * 420
                # Total dims = 1653 x 2270
                _ncx = (_xtl + _xbr) / 2 / 1653
                _ncy = (_ytl + _ybr) / 2 / 2270
                _nlx = (_xbr - _xtl) / 1653
                _nly = (_ybr - _ytl) / 2270
                file.write(f"0 {_ncx} {_ncy} {_nlx} {_nly}\n")
                
        # Save sheet music
        generate_five_staff_sheet(crop_indices=crop_indices, file_name=f'{image_file_name}.png')

    # Generate 6 staff train data
    for index in range(six_staff_sheets):
        # Generate indices
        crop_indices = np.random.randint(35, size=6)
        image_file_name = f'./Train_Sheets/images/train/six_sheet_{index}'
        label_file_name = f'./Train_Sheets/labels/train/six_sheet_{index}'
        # Save annotations
        with open(f'{label_file_name}.txt', 'w') as file:
            for _ in range(6):
                fou = six_staffs[crop_indices[_]]
                # file.write(f"0, {22 + fou['coords'][0]}, {95 + fou['coords'][1] + _ * 350}, {22 + fou['coords'][2]}, {95 + fou['coords'][3] + _ * 350}\n")
                _xtl = 22 + fou['coords'][0]
                _ytl = 95 + fou['coords'][1] + _ * 350
                _xbr = 22 + fou['coords'][2]
                _ybr = 95 + fou['coords'][3] + _ * 350
                # Total dims = 1653 x 2270
                _ncx = (_xtl + _xbr) / 2 / 1653
                _ncy = (_ytl + _ybr) / 2 / 2270
                _nlx = (_xbr - _xtl) / 1653
                _nly = (_ybr - _ytl) / 2270
                file.write(f"0 {_ncx} {_ncy} {_nlx} {_nly}\n")
        # Save sheet music
        generate_six_staff_sheet(crop_indices=crop_indices, file_name=f'{image_file_name}.png')

def parse_valid_sheets():
    with open('./Grand_Staff_Crop_Labels_Valid.json', 'r') as file:
        annotations = json.load(file)

    # Retrieve Pages
    annotations = annotations['annotations']['image']

    # Iterate over each sheet
    for sheet in annotations:
        with open(f"./Valid_Sheets/labels/{sheet['_name'][:-4]}.txt", 'w') as file:
            for label in sheet['box']:
                _ncx = (int(float(label['_xtl'])) + int(float(label['_xbr']))) / 2 / 1653
                _ncy = (int(float(label['_ytl'])) + int(float(label['_ybr']))) / 2 / 2270
                _nlx = (int(float(label['_xbr'])) - int(float(label['_xtl']))) / 1653
                _nly = (int(float(label['_ybr'])) - int(float(label['_ytl']))) / 2270
                file.write(f"0 {_ncx} {_ncy} {_nlx} {_nly}\n")

def crop_test_predictions(label_file):
    # Retrieve dimensions
    file_name = label_file.split('/')[-1]
    img = Image.open(f"./Bach_Inventions/{file_name[:-4]}.png")
    width, height = img.size

    with open(label_file, 'r') as file:
        labels = file.readlines()
    for index, label in enumerate(labels):
        _, x, y, w, l = [float(_) for _ in label.split()]
        _xtl = x - w / 2
        _xbr = x + w / 2
        _ytl = y - l / 2
        _ybr = y + l / 2
        treble = (int(_xtl * width), int(_ytl * height), int(_xbr * width), int(y * height + 5))
        bass = (int(_xtl * width), int(y * height - 5), int(_xbr * width), int(_ybr * height))
        crop_image(file=f"./Bach_Inventions/{file_name[:-4]}.png", coords=treble, output=f"./Data/{file_name[:-4]}_{index}_treble.png", dry=False)
        crop_image(file=f"./Bach_Inventions/{file_name[:-4]}.png", coords=bass, output=f"./Data/{file_name[:-4]}_{index}_bass.png", dry=False)

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--crop_staffs', action='store_true', default=False)
    parser.add_argument('--generate_sheet_music_samples', action='store_true', default=False)
    parser.add_argument('--five_staff_count', type=int, default=2500)
    parser.add_argument('--six_staff_count', type=int, default=2500)
    parser.add_argument('--parse_valid_sheets', action='store_true', default=False)
    parser.add_argument('--crop_test_predictions', action='store_true', default=False)
    parser.add_argument('--test_label_file', type=str)
    args = parser.parse_args()
    
    # Toggle functionality
    if args.crop_staffs:
        crop_staffs()
    elif args.generate_sheet_music_samples:
        generate_sheet_music_samples(args.five_staff_count, args.six_staff_count)
    elif args.parse_valid_sheets:
        parse_valid_sheets()
    elif args.crop_test_predictions:
        crop_test_predictions(args.test_label_file)
    else:
        print("You need to specify a functionality!")