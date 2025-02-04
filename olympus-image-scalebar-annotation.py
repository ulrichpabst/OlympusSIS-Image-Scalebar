import os
import sys
import tifffile
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def add_scale_bar_to_images(directory, scalecolor = 'white'):
    scaled_dir = os.path.join(directory, 'scaled')
    os.makedirs(scaled_dir, exist_ok=True)

    tiff_files = [f for f in os.listdir(directory) if f.lower().endswith(('.tif', '.tiff'))]

    for filename in tiff_files:
        file_path = os.path.join(directory, filename)

        with tifffile.TiffFile(file_path) as tif:
            image = tif.pages[0].asarray()
            tags = tif.pages[0].tags
            olympus_metadata = tags.get(33560).value
            pixelsizex = olympus_metadata.get('pixelsizex')
            pixelsizey = olympus_metadata.get('pixelsizey')
            magnification = olympus_metadata.get('magnification')
            print(f'filename: {filename}, (X): {pixelsizex * 1e9:.3f} nm/pixel, (Y): {pixelsizey * 1e9:.3f} nm/pixel, magnification: x{magnification}')


        image_width_nm = image.shape[1] * pixelsizex * 1e9

        scale_bar_options = np.array([0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000])
        scale_bar_length_nm = scale_bar_options[scale_bar_options <= image_width_nm / 10][-1]
        scale_bar_length_pixels = scale_bar_length_nm / (pixelsizex * 1e9)

        dpi = tags.get('XResolution').value[0] / tags.get('XResolution').value[1] if 'XResolution' in tags else 300
        fig, ax = plt.subplots(figsize=(image.shape[1] / dpi, image.shape[0] / dpi), dpi=dpi)

        ax.imshow(image, cmap='gray', interpolation='antialiased', vmin = 0, vmax = 65535)
        ax.axis('off')

        bar_height = max(2, int(image.shape[0] * 0.0035))
        font_size = max(8, int(image.shape[0] * 0.02))

        padding = 20
        x_pos = image.shape[1] - scale_bar_length_pixels - padding
        y_pos = image.shape[0] - bar_height - padding

        scale_bar = patches.Rectangle((x_pos, y_pos), scale_bar_length_pixels, bar_height, linewidth=0, edgecolor='none', facecolor=scalecolor)
        ax.add_patch(scale_bar)

        unit = 'µm' if scale_bar_length_nm >= 1000 else 'nm'
        label_value = scale_bar_length_nm / 1000 if unit == 'µm' else scale_bar_length_nm
        ax.text(x_pos + scale_bar_length_pixels / 2, y_pos - (font_size * 0.5), f'{label_value:g} {unit}', color=scalecolor, fontsize=font_size, ha='center', va='bottom')

        output_filename = os.path.splitext(filename)[0] + '_scaled.tif'
        output_path = os.path.join(scaled_dir, output_filename)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close()

def main():
    parser = argparse.ArgumentParser(description='Add scale bars to Olympus TIFF images')
    parser.add_argument('directory', type=str, help='Directory containing raw Olympus TIFF images')
    parser.add_argument('-c', '--color', type=str, default='white', help='Color of the scale bar (default: white, accepts any valid matplotlib color code)')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()
    add_scale_bar_to_images(args.directory, args.color)

if __name__ == '__main__': main()
