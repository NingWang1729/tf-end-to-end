#!/bin/env python3

import argparse
from PIL import Image


def crop_image():
    # Parse command line arguments
    parser = argparse.ArgumentParser(prog='Crop image from image')
    parser.add_argument('-d', '--dry-run', action='store_true', default=False, help='Dry run script without saving')
    parser.add_argument('-f', '--file-name', type=str, default='./Data/Example/000051652-1_2_1.png', help='Image name')
    parser.add_argument('-o', '--output', type=str, default='./Crops/cropped_image.png', help='Cropped image name')
    parser.add_argument('-c', '--crop', nargs=4, type=int, help='Coordinates: top, left, bottom, right')
    args = parser.parse_args()

    # Load original image
    original_image = Image.open(args.file_name)
    original_dims = original_image.size

    # Check crop dimensions
    valid_crop = True
    if args.crop is None:
        # If no region is selected, use entire image
        valid_crop = False
    elif args.crop[0] < 0 or args.crop[1] < 0:
        # Top left coordinate is invalid
        valid_crop = False
    elif args.crop[2] > original_dims[0] or args.crop[3] > original_dims[1]:
        # Bottom right coordinate is invalid
        valid_crop = False

    # Convert crop coordinates to tuple
    if valid_crop:
        # Use crop coordinates
        args.crop = (args.crop[0], args.crop[1], args.crop[2], args.crop[3])
    else:
        # Do not crop image at all
        args.crop = (0, 0, original_dims[0], original_dims[1])

    # Crop image
    cropped_image = original_image.crop(args.crop)

    # Just testing things out
    if args.dry_run:
        print(f'Original_dims were {original_dims}')
        print(f'New dimensions are {cropped_image.size}')
        cropped_image.show()
    else:
        cropped_image.save(args.output)


if __name__ == '__main__':
    crop_image()