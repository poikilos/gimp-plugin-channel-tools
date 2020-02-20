#!/usr/bin/env python
from channel_tinker import diff_images
from PIL import Image
from channel_tinker import error

def diff_images_by_path(base_path, head_path, diff_path=None):
    """
    Compare two images.

    Keyword arguments:
    diff_path -- If not None, then save a graphical representation of
    the difference: black is same, closer to white differs (if images
    are different sizes, red is deleted, green is added).
    """
    base = Image.open(base_path)
    head = Image.open(head_path)
    w = max(base.size[0], head.size[0])
    h = max(base.size[1], head.size[1])
    diff_size = w, h
    diff = None
    # draw = None
    nochange_color = (0, 0, 0, 255)
    if diff_path is not None:
        diff = Image.new('RGBA', diff_size, nochange_color)
        # error("* generated diff image in memory")
        # draw = ImageDraw.Draw(diff)
    error("Checking {} zone...".format(diff_size))
    result = diff_images(base, head, diff_size, diff=diff,
                         nochange_color=nochange_color)
    if diff_path is not None:
        diff.save(diff_path)
        error("* saved {}".format(diff_path))
    return result


