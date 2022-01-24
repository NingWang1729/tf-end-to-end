#!/bin/env python3

import re
import json
import numpy as np

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
        file_name = f'./Train_Sheets/five_sheet_{index}'
        # Save annotations
        with open(f'{file_name}.csv', 'w') as file:
            for _ in range(5):
                fou = five_staffs[crop_indices[_]]
                file.write(f"0, {22 + fou['coords'][0]}, {95 + fou['coords'][1] + _ * 420}, {22 + fou['coords'][2]}, {95 + fou['coords'][3] + _ * 420}\n")

        # Save sheet music
        generate_five_staff_sheet(crop_indices=crop_indices, file_name=f'{file_name}.png')

    # Generate 6 staff train data
    for index in range(six_staff_sheets):
        # Generate indices
        crop_indices = np.random.randint(35, size=6)
        file_name = f'./Train_Sheets/six_sheet_{index}'
        # Save annotations
        with open(f'{file_name}.csv', 'w') as file:
            for _ in range(6):
                fou = six_staffs[crop_indices[_]]
                file.write(f"0, {22 + fou['coords'][0]}, {95 + fou['coords'][1] + _ * 350}, {22 + fou['coords'][2]}, {95 + fou['coords'][3] + _ * 350}\n")

        # Save sheet music
        generate_six_staff_sheet(crop_indices=crop_indices, file_name=f'{file_name}.png')


if __name__ == '__main__':
    # crop_staffs()
    generate_sheet_music_samples(1000, 1000)
    pass