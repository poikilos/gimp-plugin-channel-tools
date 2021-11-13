#!/usr/bin/env python
'''
Compare two images. Provide a dictionary such as:
{
  "same": false,
  "base": {
    "size": [
      16,
      128
    ],
    "ratio": 0.125
  },
  "head": {
    "size": [
      16,
      128
    ],
    "ratio": 1.0
  },
  "diff": {
    "path": "/home/owner/minetest/diffimage in bucket_game-200527 vs in bucket_game.png"
  }
}

'''
import os

from channel_tinker import diff_images
from PIL import Image
import PIL
from channel_tinker import (
    error,
    debug,
)


def diff_images_by_path(base_path, head_path, diff_path=None):
    """
    Compare two images.

    Keyword arguments:
    diff_path -- If not None, then save a graphical representation of
    the difference: black is same, closer to white differs (if images
    are different sizes, red is deleted, green is added).
    """
    result = None
    try:
        base = Image.open(base_path)
    except PIL.UnidentifiedImageError:
        result = {
            'base': {
                'error': "UnidentifiedImageError"
            },
            'head': {
            },  # It must be a dict to prevent a key error.
        }
    try:
        head = Image.open(head_path)
    except PIL.UnidentifiedImageError:
        result2 = {
            'base': {
            },  # It must be a dict to prevent a key error.
            'head': {
                'error': "UnidentifiedImageError"
            }
        }
        if result is None:
            result = result2
        else:
            result['head'] = result2['head']
    if result is not None:
        # Return an error.
        return result
    w = max(base.size[0], head.size[0])
    h = max(base.size[1], head.size[1])
    diff_size = w, h
    debug("* base size:{}".format(base.size))
    debug("* head size:{}".format(head.size))
    diff = None
    # draw = None
    nochange_color = (0, 0, 0, 255)
    if diff_path is not None:
        diff = Image.new('RGBA', diff_size, nochange_color)
        # error("* generated diff image in memory")
        # draw = ImageDraw.Draw(diff)
        error("* diff size:{}".format(diff.size))
    debug("Checking {} zone...".format(diff_size))
    result = diff_images(base, head, diff_size, diff=diff,
                         nochange_color=nochange_color)
    if diff_path is not None:
        diff_path = os.path.abspath(diff_path)
        diff.save(diff_path)
        result['diff'] = {}
        result['diff']['path'] = diff_path
        error("* saved \"{}\"".format(diff_path))
    return result


