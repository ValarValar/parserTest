import os
import sys

from PIL import Image

DATA_PATH = "image_processing_data/"


def process_images(source, shape, result):
    """Paste shape image upper then source in one file.
    Arguments:
    • source — src to image, that should be under shape.
    • shape — src to image, that we place into source.
    • result — src to output file.
    Usage:
    >>> process_images('source.jpg', 'shape.png', 'output.jpg')
    • Return None
    • Result image is on src 'output.jpg'
    """

    source_i = Image.open(source)
    shape_i = Image.open(shape)

    # Get sizes of images
    source_w, source_h = source_i.size
    shape_w, shape_h = shape_i.size

    # Calculate full size of result image
    result_w = shape_w if shape_w > source_w else source_w
    result_h = shape_h + source_h

    # Create new image
    result_i = Image.new('RGB', (result_w, result_h))

    # Fill in with color white color (255, 255, 255)
    result_i.paste((255, 255, 255), [0, 0, result_w, result_h])

    # Paste images to new result image
    result_i.paste(source_i, ((result_w - source_w) // 2, shape_h))
    result_i.paste(shape_i, ((result_w - shape_w) // 2, 0))

    # Save result image to passed filename
    result_i.save(result, quality=100)


def check_files(*args):
    """Check all given files for existing.
    Arrtibutes:
    • *args — any number of args, that should be strings.
    Return:
    • True if all files exist.
    • False if any of the file doesn't exist.
    Usage:
    >>> result = check_files('file1', 'file2', 'file3')  # True or False
    """
    for src in args:
        if not isinstance(src, str):
            raise TypeError(f'All args must be str, not {type(src)}')

        if not os.path.isfile(src):
            return False
    return True


if __name__ == '__main__':

    if not len(sys.argv) == 4:
        print(f'Not valid count of args. Must be 3, but given {len(sys.argv)}')
        print('usage: python script.py [source.jpg] [shape.png] [result.jpg]')
        raise SystemExit
    source_src, shape_src, result_src = DATA_PATH + sys.argv[1], \
                                        DATA_PATH + sys.argv[2], \
                                        DATA_PATH + sys.argv[3]
    if check_files(source_src, shape_src):
        process_images(source_src, shape_src, result_src)
        print(f'Successfuly placed new image: {result_src}')
    else:
        print('One of the file doesn\'t exist')
        print('usage: python script.py [source.jpg] [shape.png] [result.jpg]')
