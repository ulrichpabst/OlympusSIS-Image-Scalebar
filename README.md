# OlympusSIS-Image-Scalebar
A python script that automatically adds scale bars to OlympusSIS electron microscopy raw images.

## Usage

In the terminal, simply run `python olympus-image-scalebar-annotation.py`. This will yield the general help message:

```bash
usage: olympus-image-scalebar-annotation.py [-h] [-c COLOR] directory

Add scale bars to Olympus TIFF images

positional arguments:
  directory             Directory containing raw Olympus TIFF images

options:
  -h, --help            show this help message and exit
  -c COLOR, --color COLOR
                        Color of the scale bar (default: white, accepts any valid matplotlib color code)
```

## Example Image

