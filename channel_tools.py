#!/usr/bin/env python
"""
For each pixel where the alpha is below the threshold, get a new color
using the nearest opaque pixel.
"""
from gimpfu import *  # by convention, import *

from channel_tools import extend
from channel_tools import draw_square_from_center
from channel_tools import draw_circle_from_center

def remove_layer_halo(image, drawable, minimum, maximum, good_minimum,
                      make_opaque, enable_threshold, threshold):
    gimp.progress_init("This may take a while...")
    # print("options: {}".format((str(image), str(drawable), str(minimum),
    #                            str(maximum), str(make_opaque),
    #                            str(good_minimum))))
    extend(image=image, drawable=drawable, minimum=minimum,
           maximum=maximum, make_opaque=make_opaque,
           good_minimum=good_minimum, enable_threshold=enable_threshold,
           threshold=threshold)
    # draw_square_from_center((4,4), 2, image=image, drawable=drawable,
    #                         color=(255,0,0,255))
    # draw_square_from_center((4,4), 4, image=image, drawable=drawable,
    #                         color=(0,255,0,255))
    # draw_square_from_center((4,4), 0, image=image, drawable=drawable)
    # draw_square_from_center((4,4), 0, image=image, drawable=drawable,
    #                         color=(0,0,0,255), filled=True)
    # draw_circle_from_center((128,128), 32, image=image,
    #                         drawable=drawable,
    #                         color=(255,0,0,255), filled=True)
    # draw_square_from_center((1,1), 2, image=image, drawable=drawable,
    #                         color=(0,0,255,255))
    # print("updating image...")
    pdb.gimp_displays_flush()
    # ^ update the image; only works since the called method already
    # has called pdb.gimp_drawable_update(...).
    # print("done (remove_layer_halo)")

max_tip = "Maximum to discard (254 unless less damaged)"
goot_min_tip = "get nearby >= this (usually max discard+1)."
m_o_tip = "Make the fixed parts opaque."
a_t_tip = "Apply the threshold below to the image."
t_tip = "Minimum alpha to set to 255"
# See https://www.youtube.com/watch?v=uSt80abcmJs
register(
    "python_fu_remove_halo",
    "Remove Halo",
    "Remove alpha",
    "Jake Gustafson", "Jake Gustafson", "2020",
    "Remove Halo",  # caption
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
    remove_layer_halo,
    menu="<Image>/Layer/Channel Tools"
)

main()
