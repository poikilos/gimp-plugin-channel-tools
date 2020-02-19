# channel_tools
Manipulate color and alpha using new "Channel Tools" in the GIMP "Layer"
menu.

## Install
### Linux
```
if [ -d ~/.config/GIMP/2.10/plug-ins/channel_tools.py ]; then
    rm ~/.config/GIMP/2.10/plug-ins/channel_tools.py
fi
cp channel_tools.py ~/.config/GIMP/2.10/plug-ins/
if [ -d ~/.config/GIMP/2.10/plug-ins/channel_tools ]; then
    rm ~/.config/GIMP/2.10/plug-ins/channel_tools  # try symlink FIRST
    rm -Rf ~/.config/GIMP/2.10/plug-ins/channel_tools
fi
cp -R channel_tools ~/.config/GIMP/2.10/plug-ins/
#or
ln -s ~/git/gimp-plugin-channel-tools/channel_tools.py ~/.config/GIMP/2.10/plug-ins/
ln -s ~/git/gimp-plugin-channel-tools/channel_tools ~/.config/GIMP/2.10/plug-ins/
```

## Developer Notes

### Python-fu sites
- [API Documentation](https://www.gimp.org/docs/python/index.html)
- [Gimp Scripting: Python Fu, Automating Workflows, coding a complete plug-in](https://www.youtube.com/watch?v=uSt80abcmJs) by Jason Bates Sep 13, 2015
- [Python fu #6: Accepting user input](https://jacksonbates.wordpress.com/2015/09/14/python-fu-6-accepting-user-input/) by Jason Bates


### GIMP API
- Booleans (non-zero if true):
  - drawable.is_color
  - drawable.has_alpha
  - drawable.is_gray
  - drawable.is_indexed
  - drawable.visible
- Other
  - image.active_channel (assignable)
  - image.cmap (color map)
  - image.layers (list of layers)
  - image.selection (selection mask)
  - image.add_layer_mask(layer, mask)

