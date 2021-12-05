# channel_tinker (and GIMP Plugin)
<https://github.com/poikilos/gimp-plugin-channel-tinker>

This package contains a generalized advanced color channel manipulation
module called channel_tinker that is currently only available here.

In GIMP, you can manipulate color and alpha using new "Channel Tinker"
sub-menu in the GIMP "Colors" menu.


## Install
### Linux
```
if [ -f ~/.config/GIMP/2.10/plug-ins/channel_tinker.py ]; then
    rm ~/.config/GIMP/2.10/plug-ins/channel_tinker.py
fi
cp channel_tinker_gimp.py ~/.config/GIMP/2.10/plug-ins/
if [ -d ~/.config/GIMP/2.10/plug-ins/channel_tinker ]; then
    rm ~/.config/GIMP/2.10/plug-ins/channel_tinker  # try symlink FIRST
    if [ $? -ne 0 ]; then
        # If there was an error, assume it is a directory:
        rm -Rf ~/.config/GIMP/2.10/plug-ins/channel_tinker
    fi
fi
cp -R channel_tinker ~/.config/GIMP/2.10/plug-ins/
#or
ln -s ~/git/gimp-plugin-channel-tinker/channel_tinker_gimp.py ~/.config/GIMP/2.10/plug-ins/
ln -s ~/git/gimp-plugin-channel-tinker/channel_tinker ~/.config/GIMP/2.10/plug-ins/
ls -l ~/.config/GIMP/2.10/plug-ins/channel_tinker
```


## Developer Notes

### How to Help
- ChannelTinkerProgressInterface and ChannelTinkerInterface are
  available so that far less duck typing is necessary to work with
  radically different backends such as PIL and GIMP. You can make the
  channel_tinker work with additional things beyond PIL and GIMP by
  making your own implementation. See channel_tinker_gimp for an
  example.
  - You do not have to implement ChannelTinkerInterface if you provide
    the functions in channel_tinker with a PIL image.
  - You do not have to implement ChannelTinkerProgressInterface if you
    simply do not provide a ctpi argument to the channel_tinker
    functions.

### Tasks
- [ ] Add hotkey 'r' for Channel Tinker (not yet taken in top level of
  Colors menu).

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

