# channel_tools
This is a GIMP plugin with tools for manipulating color and alpha.

## Install
### Linux
```
if [ -d ~/.config/GIMP/2.10/plug-ins/channel_tools.py ]; then
    rm ~/.config/GIMP/2.10/plug-ins/channel_tools.py
fi
cp channel_tools.py ~/.config/GIMP/2.10/plug-ins/
if [ -d ~/.config/GIMP/2.10/plug-ins/channel_tools ]; then
    rm -Rf ~/.config/GIMP/2.10/plug-ins/channel_tools
fi
cp -R channel_tools ~/.config/GIMP/2.10/plug-ins/
#or
#ln -s ~/git/channel_tools/channel_tools.py ~/.config/GIMP/2.10/plug-ins/
#ln -s ~/git/channel_tools/channel_tools ~/.config/GIMP/2.10/plug-ins/
```
