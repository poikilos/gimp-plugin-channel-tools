#!/usr/bin/env python
"""
For each pixel where the alpha is below the threshold, get a new color
using the nearest opaque pixel.
"""
from gimpfu import *  # by convention, import *

from channel_tools import extend
from channel_tools import draw_square_from_center
from channel_tools import draw_circle_from_center
from channel_tools import convert_depth


def ct_draw_centered_circle(image, drawable, radius, color, filled):
    image.disable_undo()
    w = pdb.gimp_image_width(image)
    h = pdb.gimp_image_height(image)
    x = None
    y = None

    if w % 2 == 1:
        x = float(w) / 2.0
    else:
        x = w / 2
    if h % 2 == 1:
        y = float(h) / 2.0
    else:
        y = h / 2
    expand_right = False  # TODO: implement this
    expand_down = False  # TODO: implement this
    post_msg = ""
    if (w % 2 == 0):
        expand_right = True
        post_msg = "horizontally"
    if (h % 2 == 0):
        expand_down = True
        if len(post_msg) > 0:
            post_msg += " or "
        post_msg += "vertically"

    if len(post_msg) > 0:
        msg = ("The image is an even number of pixels, so the current"
               " drawing function cannot draw exactly centered"
               " " + post_msg + ".")
        pdb.gimp_message(msg)

    draw_circle_from_center((x, y), radius, image=image,
                            drawable=drawable,
                            color=color, filled=filled)
    pdb.gimp_drawable_update(drawable, 0, 0, drawable.width,
                             drawable.height)
    pdb.gimp_displays_flush()
    image.enable_undo()

def ct_draw_centered_square(image, drawable, radius, color, filled):
    image.disable_undo()
    w = pdb.gimp_image_width(image)
    h = pdb.gimp_image_height(image)
    x = w // 2
    y = h // 2
    expand_right = False  # TODO: implement this
    expand_down = False  # TODO: implement this
    post_msg = ""
    if (w % 2 == 0):
        expand_right = True
        post_msg = "horizontally"
    if (h % 2 == 0):
        expand_down = True
        if len(post_msg) > 0:
            post_msg += " or "
        post_msg += "vertically"

    if len(post_msg) > 0:
        msg = ("The image is an even number of pixels, so the current"
               " drawing function cannot draw exactly centered"
               " " + post_msg + ".")
        pdb.gimp_message(msg)

    print("image.channels: {}".format(image.channels))
    print("image.base_type: {}".format(image.channels))

    draw_square_from_center((x, y), radius, image=image,
                            drawable=drawable, color=color,
                            filled=filled)
    pdb.gimp_drawable_update(drawable, 0, 0, drawable.width,
                             drawable.height)
    pdb.gimp_displays_flush()
    image.enable_undo()


def ct_remove_layer_halo(image, drawable, minimum, maximum, good_minimum,
                         make_opaque, enable_threshold, threshold):
    gimp.progress_init("This may take a while...")
    # print("options: {}".format((str(image), str(drawable), str(minimum),
    #                            str(maximum), str(make_opaque),
    #                            str(good_minimum))))
    extend(image=image, drawable=drawable, minimum=minimum,
           maximum=maximum, make_opaque=make_opaque,
           good_minimum=good_minimum, enable_threshold=enable_threshold,
           threshold=threshold)
    pdb.gimp_drawable_update(drawable, 0, 0, drawable.width,
                             drawable.height)
    pdb.gimp_displays_flush()
    # ^ update the image; still you must first do#
    # pdb.gimp_drawable_update(...)
    image.enable_undo()

max_tip = "Maximum to discard (254 unless less damaged)"
goot_min_tip = "get nearby >= this (usually max discard+1)."
m_o_tip = "Make the fixed parts opaque."
a_t_tip = "Apply the threshold below to the image."
t_tip = "Minimum alpha to set to 255"
# See "Python-fu sites" under "Developer Notes" in README.md
register(
    "python_fu_ct_remove_halo",
    "Remove Halo",  # short description
    "Remove alpha",  # long description
    "Jake Gustafson", "Jake Gustafson", "2020",
    "Remove Halo",  # menu item caption
    "RGBA",  # RGB* would mean with or without alpha.
    [
        (PF_IMAGE, "image", "Current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
        (PF_SPINNER, "minimum", "Minimum alpha to fix (normally 1)", 1,
         (0, 255, 1)),
        (PF_SPINNER, "maximum", max_tip, 254, (0, 255, 1)),
        (PF_SPINNER, "good_minimum", goot_min_tip, 255, (0, 255, 1)),
        (PF_TOGGLE, "make_opaque", m_o_tip, False),
        (PF_TOGGLE, "enable_threshold", a_t_tip, False),
        (PF_SPINNER, "threshold", t_tip, 128, (0, 255, 1))
    ],
    [], # results
    ct_remove_layer_halo,
    menu="<Image>/Layer/Channel Tools"
)

# register(
    # "python_fu_ct_centered_circle",
    # "Draw Centered Circle",
    # "Draw centered circle",
    # "Jake Gustafson", "Jake Gustafson", "2020",
    # "Draw Centered Circle",  # caption
    # "RGB*",  # RGB* would mean with or without alpha.
    # [
        # (PF_IMAGE, "image", "Current image", None),
        # (PF_DRAWABLE, "drawable", "Input layer", None),
        # (PF_INT,    "radius", "Radius", 15),
        # (PF_COLOR,  "color", "Color", (0, 0, 0)),
        # (PF_TOGGLE, "filled", "Filled", False),
    # ],
    # [], # results
    # ct_draw_centered_circle,
    # menu="<Image>/Layer/Channel Tools"
# )


register(
    "python_fu_ct_centered_square",
    "Draw Centered Square",
    "Draw centered square",
    "Jake Gustafson", "Jake Gustafson", "2020",
    "Draw Centered Square",  # caption
    "RGB*",  # RGB* would mean with or without alpha.
    [
        (PF_IMAGE, "image", "Current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
        (PF_INT,    "radius", "Radius", 15),
        (PF_COLOR,  "color", "Color", (0, 0, 0)),
        (PF_TOGGLE, "filled", "Filled", False),
    ],
    [], # results
    ct_draw_centered_square,
    menu="<Image>/Layer/Channel Tools"
)

main()
