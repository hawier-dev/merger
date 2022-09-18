# Merger

![Splitter showcase](./showcase.gif)

Image manipulation tool to merge **tiled image** into one image.

Inspired by: [pnytko/merger](https://github.com/pnytko/merger)

## Requirements

```bash
python3
numpy
natsort
pillow
rich # optional
```

## Using

Merging image.

```bash
python merger.py --path {path_to_folder_with_tiles} --out {output_path}
```

Example directory content:

```bash
# Where 0_0 = HORIZONTAL-INDEX_VERTICAL-INDEX
image_name_0_0.jpg
image_name_0_1.jpg
image_name_0_2.jpg
image_name_1_0.jpg
image_name_1_1.jpg
image_name_1_2.jpg
image_name_2_0.jpg
image_name_2_1.jpg
image_name_2_2.jpg
```
