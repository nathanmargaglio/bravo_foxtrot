#!/bin/bash
if [ ! -d "$gifs" ]; then
        mkdir gifs
fi
ffmpeg -y -i ~/everything/logs/"$1"/img/%d.png -vf palettegen ~/everything/logs/"$1"/img/palette.png
ffmpeg -y -framerate 6 -i ~/everything/logs/"$1"/img/%d.png -i ~/everything/logs/"$1"/img/palette.png -lavfi paletteuse ~/everything/logs/gifs/"$1$2".gif
