#!/usr/bin/env python3
'''
Compare two image files.

Similar projects:
- diffimg
'''
import sys
import os
# from PIL import ImageDraw
import json

from channel_tinker_pil import diff_images_by_path
from channel_tinker import (
    generate_diff_name,
    error,
)


def run(base_path, head_path, diff_name=None):
    if diff_name is None:
        diff_name = generate_diff_name(base_path, head_path)
    results = diff_images_by_path(base_path, head_path,
                                  diff_path=diff_name)
    print(json.dumps(results, indent=2))
    return results


def main():
    if len(sys.argv) != 3:
        error("You must specify two files.")
        exit(1)
    results = run(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()

