"""
Merge all images in a folder into one image.

Usage:
    python merger.py --path <image_path> --out <out_path>

Example:
    python merger.py --path /home/user/images --out /home/user/
"""
from os.path import basename

import numpy as np
import argparse
import os
import re
from PIL import Image
from natsort import natsorted


def parse_args():
    parser = argparse.ArgumentParser("Merge all images in a folder into one image")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        required=True,
        help="Path to the folder containing the images",
    )
    parser.add_argument(
        "-o", "--out", type=str, required=True, help="Path to the output folder"
    )
    args = parser.parse_args()

    if (
        os.path.isdir(args.path)
        and len(re.findall("_tiled[0-9]+", args.path)) == 0
        and not args.path.endswith("_tiled")
    ):
        split_dirs = [
            os.path.join(args.path, split_dir)
            for split_dir in os.listdir(args.path)
            if os.path.isdir(os.path.join(args.path, split_dir))
            if split_dir.endswith("_tiled")
            or len(re.findall("_tiled[0-9]+", split_dir)) > 0
        ]
    elif os.path.isdir(args.path):
        split_dirs = [args.path]
    else:
        split_dirs = []

    print(split_dirs)

    if not split_dirs:
        print("No tiled images found in the specified directory.")
        exit(1)

    return split_dirs, args.out


def check_image_file(image):
    image_extensions = [".jpg", ".jpeg", ".tif", ".bmp", ".png", ".gif"]
    for image_ext in image_extensions:
        if image.endswith(image_ext):
            return True
    return False


def group_images(images, image_ext):
    all_images = natsorted(images)
    last_y = 0
    group_index = 0
    grouped_images = [[]]
    for image in all_images:
        if image.endswith(image_ext):
            image_name_no_ext = image.replace("." + image_ext, "")
            coord_y = image_name_no_ext.split("_")[-2]
            if int(coord_y) == last_y:
                grouped_images[group_index].append(os.path.join(image))
            else:
                grouped_images.append([image])
                group_index += 1
                last_y = int(coord_y)

    return grouped_images


def merge(grouped_images):
    horizontal_parts = []
    for group in grouped_images:
        images = [Image.open(image) for image in group]
        horizontal_part = np.hstack((np.asarray(image) for image in images))
        horizontal_parts.append(Image.fromarray(horizontal_part))

    full_image = np.vstack((np.asarray(image) for image in horizontal_parts))
    full_image = Image.fromarray(full_image)

    return full_image


def main():
    split_dirs, out_path = parse_args()
    for split_dir in split_dirs:
        all_images = [
            os.path.join(split_dir, image)
            for image in os.listdir(split_dir)
            if check_image_file(image)
        ]
        image_ext = all_images[0].split(".")[-1]
        image_name = basename(all_images[0]).replace(
            re.findall(f"_[0-9]+_[0-9]+.{image_ext}", all_images[0])[-1], ""
        )

        grouped_images = group_images(all_images, image_ext)
        full_image = merge(grouped_images)

        image_ext = all_images[0].split(".")[-1]
        full_image.save(os.path.join(out_path, image_name + "_merged." + image_ext))


if __name__ == "__main__":
    main()
