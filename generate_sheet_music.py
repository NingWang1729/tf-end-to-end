#!/bin/env python3

import numpy as np

from PIL import Image

def test():
    generate_five_staff_sheet()
    generate_six_staff_sheet()

def generate_five_staff_sheet(crop_indices=None, crop_count=35, file_name=None):
    left_margin = 22
    top_margin = 95
    sheet = Image.new('RGB', (1653, 2270), (255, 255, 255))
    if crop_indices is None:
        crop_indices = np.random.randint(crop_count, size=5)
    crop_files = [f'./Crops/five_{_}.png' for _ in crop_indices]
    crop_images = [Image.open(_) for _ in crop_files]
    for index, image in enumerate(crop_images):
        sheet.paste(image, (left_margin, top_margin + index * 420))
    if file_name is None:
        sheet.show()
    else:
        sheet.save(file_name)

def generate_six_staff_sheet(crop_indices=None, crop_count=66, file_name=None):
    left_margin = 22
    top_margin = 95
    sheet = Image.new('RGB', (1653, 2270), (255, 255, 255))
    if crop_indices is None:
        crop_indices = np.random.randint(crop_count, size=6)
    crop_files = [f'./Crops/six_{_}.png' for _ in crop_indices]
    crop_images = [Image.open(_) for _ in crop_files]
    for index, image in enumerate(crop_images):
        sheet.paste(image, (left_margin, top_margin + index * 350))
    if file_name is None:
        sheet.show()
    else:
        sheet.save(file_name)

if __name__ == '__main__':
    test()