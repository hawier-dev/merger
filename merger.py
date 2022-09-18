# Image manipulation tool to merge tiled image into one image.
# python ~/scripts/merger.py --path__Path --out__Output_path


import numpy as np
import argparse
import os
import warnings
import re
import sys
from PIL import Image
from natsort import natsorted

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, required=True)
parser.add_argument("--out", type=str, required=True)
args = parser.parse_args()


rich_printing = True
try:
    from rich.console import Console
    from rich import print
    from rich.text import Text
    from rich.panel import Panel
    from rich.pretty import pprint
except ImportError:
    rich_printing = False

platform_path = '/'
if sys.platform =='win32':
    platform_path = '\\'

image_path = args.path[:-1] if args.path.endswith(platform_path) else args.path
out_path = args.out[:-1] if args.out.endswith(platform_path) else args.out

all_images = [image for image in os.listdir(image_path)]
all_images = natsorted(all_images)

image_ext = all_images[0].split('.')[-1]
image_name = all_images[0].replace(re.findall(
    f'_[0-9]+_[0-9]+.{image_ext}', all_images[0])[-1], '')


def print_rich_image_info():
    # Image info
    console = Console()

    # title of image panel
    panel_title_text = Text()
    panel_title_text.append("MERGE", style='green')

    # image name
    image_name_text = Text()
    image_name_text.append("Image Name: ")
    image_name_text.append(image_name + f'.{image_ext}', style='blue')

    print(Panel.fit(image_name_text, style='bold', title=panel_title_text))
    text = Text()
    text.append("Tile count: ")
    text.append(f"{len(all_images)}\n", style='bold blue')
    text.append("Extension: ")
    text.append(f"{image_ext}\n", style='bold blue')
    console.print(text)


def print_image_info():
    # Image info
    print(f"Image Name: {image_name}.{image_ext}\n")
    print(f"Tile count: {len(all_images)}\n")
    print(f"Extension: {image_ext}\n")


if rich_printing:
    print_rich_image_info()
else:
    print_image_info()


def group_images():
    last_y = 0
    group_index = 0
    grouped_images = [[]]
    for image in all_images:
        image_name_no_ext = image.replace('.' + image.split('.')[-1], '')
        coord_y = image_name_no_ext.split('_')[-2]
        if int(coord_y) == last_y:
            grouped_images[group_index].append(image_path + platform_path + image)
        else:
            grouped_images.append([image_path + platform_path + image])
            group_index += 1
            last_y = int(coord_y)

    return grouped_images


def merge(grouped_images):
    horizontal_parts = []
    for group in grouped_images:
        images = [Image.open(image) for image in group]
        # image_shape = sorted([(np.sum(image.size), image.size)
        #                      for image in images])[0][1]
        horizontal_part = np.hstack(
            (np.asarray(image) for image in images))
        horizontal_parts.append(Image.fromarray(horizontal_part))

    full_image = np.vstack((np.asarray(image) for image in horizontal_parts))
    full_image = Image.fromarray(full_image)

    return full_image


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        grouped_images = group_images()
        full_image = merge(grouped_images)
        full_image.save(f'{out_path}{platform_path}{image_name}.{image_ext}')
        if rich_printing:
            console = Console()
            text = Text()
            text.append("< Done >\n", style="bold green")
            text.append(f"Zapisano: ", style='bold')
            text.append(f'{out_path}{platform_path}{image_name}.{image_ext}\n',
                        style="bold green")
            console.print(text)
        else:
            print('\nDone')
            print(f'Zapisano: {out_path}{platform_path}{image_name}.{image_ext}\n')

    except Exception as err:
        if rich_printing:
            console = Console()
            text = Text()
            text.append(f"Error: ", style="bold red")
            text.append(f"{err}\n", style="bold white")
            console.print(text)
        else:
            print(f'Error: {err}\n')
