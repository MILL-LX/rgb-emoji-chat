# Application Assets

## Emoji Glyph PNGs

Assets in the [emoji-glyphs/64x64](emoji-glyphs/64x64) folder were created by rendering the .png files from the .svg files provided by [Twemoji](https://github.com/twitter/twemoji). This is done using the [Inkscape](https://inkscape.org/) CLI. The command line below renders the PNGs in the desired size with a transparent background:

```bash
find . -name "*.svg" -print0 | xargs -0 -I {} sh -c 'inkscape "{}" --export-filename="../64x64/$(basename "{}" .svg).png" --export-width=64 --export-height=64 --export-background=#000000'
```
