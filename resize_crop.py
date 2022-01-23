#!/bin/env python3

import os
import re
from PIL import Image


def main(path='./Crops'):
    crop_list = os.listdir(path)
    for crop in crop_list:
        resize_crop(f'{path}/{crop}')


def resize_crop(file=None):
    # Open file
    img = Image.open(file)

    # Resize based on staff count
    if re.search('five', file):
        img = img.resize((1600, 400))
    elif re.search('six', file):
        img = img.resize((1600, 333))

    # Save file
    img.save(file)


if __name__ == '__main__':
    main()