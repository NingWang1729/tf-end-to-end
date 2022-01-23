#!/bin/env python3

import json
from image_cropper import crop_image

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


if __name__ == '__main__':
    crop_staffs()