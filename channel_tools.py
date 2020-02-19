#!/usr/bin/env python
"""
For each pixel where the alpha is below the threshold, get a new color
using the nearest opaque pixel.
"""
from gimpfu import *  # by convention, import *

from channel_tools import extend
# from channel_tools import draw_square_from_center

def remove_layer_halo(image, drawable, minimum, maximum, good_minimum,
                      make_opaque):
    gimp.progress_init("This may take a while...")
    print("options: {}".format((str(image), str(drawable), str(minimum),
                               str(maximum), str(make_opaque),
                               str(good_minimum))))
    extend(image=image, drawable=drawable, minimum=minimum,
           maximum=maximum, make_opaque=make_opaque,
           good_minimum=good_minimum)
    # draw_square_from_center((4,4), 2, image=image, drawable=drawable,
    #                         color=(255,0,0,255))
    # draw_square_from_center((4,4), 4, image=image, drawable=drawable,
    #                         color=(0,255,0,255))
    # draw_square_from_center((4,4), 0, image=image, drawable=drawable)
    # draw_square_from_center((1,1), 2, image=image, drawable=drawable,
    #                         color=(0,0,255,255))
    print("updating image...")
    pdb.gimp_displays_flush()  # update the image; doesn't work
    print("done (remove_layer_halo)")

max_tip = "Maximum alpha to fix (normally 254 unless less damaged)"
goot_min_tip = "Find a nearby color >= this (usually maximum+1)."
m_o_tip = "Make the fixed parts opaque."
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
        (PF_TOGGLE, "make_opaque", m_o_tip, False)
    ],
    [], # results
    remove_layer_halo,
    menu="<Image>/Layer"
)

main()
