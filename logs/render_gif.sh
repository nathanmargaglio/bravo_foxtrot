#!/bin/bash
if [ ! -d "$gifs" ]; then
        mkdir gifs
fi
ffmpeg -y -i "$1"/img/%d.png -vf palettegen "$1"/img/palette.png
ffmpeg -y -framerate 6 -i "$1"/img/%d.png -i "$1"/img/palette.png -lavfi paletteuse gifs/"$1$2".gif
