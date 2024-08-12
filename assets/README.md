Assets in the 64x64 folder were created by rendering the .png files from the .svg files provided by [Twemoji](https://github.com/twitter/twemoji)

This was done using inkscape on a mac laptop using:

```bash
find . -name "*.svg" -print0 | xargs -0 -I {} sh -c 'inkscape "{}" --export-filename="../64x64/$(basename "{}" .svg).png" --export-width=64 --export-height=64'

```
