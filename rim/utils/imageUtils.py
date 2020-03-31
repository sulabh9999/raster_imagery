# image utilities
import numpy as np
import collections
from PIL import Image

# raster
from rasterio.features import rasterize
import rasterio
from rasterio.windows import Window


def total_chunks_in_image(tif, window, stride):
    rst = rasterio.open(tif)

    res_height = rst.meta['height']
    res_width = rst.meta['width']

    w_h = window[0]
    w_w = window[1]

    s_h = stride[0]
    s_w = stride[1]

    if s_h > w_h or s_w > w_w:
        raise ValueError('Incorrect stried or window dimension')

    h = res_height // s_h
    w = res_width // s_w

    return h * w


# frame: (2353, 5674) image frame size (h, w)
# window_size: (512 512) size of window (h, w)
# stride: (10, 10) vertical and horizontal jump for each stride
def sliding_window_numbers(frame, window_size, stride):
    """
	- An image frame is a large image frame(height, width)
	- method yields only frame number of small image pices 
	"""
    if not frame or len(frame) != 2:
        raise ValueError(f'Incorrect image frame {frame}, expected (h,w)')

    if not window_size or len(window_size) != 2:
        raise ValueError(
            f'Incorrect window size {window_size}, expected (h, w)')

    i_height = frame[0]
    i_width = frame[1]

    w_height = window_size[1]
    w_width = window_size[0]

    # print(i_height, i_width, frame)
    assert i_height, 'Image frame height is None'
    assert i_width, 'Image frame width is None'

    assert w_width, 'Window width is None'
    assert w_height, 'Window height is None'

    x_stride = w_width
    y_stride = w_height

    if stride and len(stride) == 2:
        y_stride = stride[0]
        x_stride = stride[1]

    frm = collections.namedtuple('Frame', ['x', 'y', 'width', 'height'])
    for y in range(0, i_height - w_height + 1, y_stride):
        for x in range(0, i_width - w_width + 1, x_stride):
            yield frm(x, y, w_width, w_height)


def is_full_white_image(arr):
    """
	true: if image contains ONLY white color
	"""
    return np.mean(arr) == 0.0


def get_image_chunks(tif, window_size, stride, count=-1):
    """
	Cut images into chunks using sliding window.
	"""
    rst = rasterio.open(tif)

    res_height = rst.meta['height']
    res_width = rst.meta['width']

    # get sliding window numbers
    for index, frame in enumerate(
            sliding_window_numbers(frame=(res_height, res_width),
                                   window_size=window_size,
                                   stride=stride)):
        window = Window(frame.x, frame.y, frame.width, frame.height)
        res_img_arr = rst.read(window=window)

        if count == 0:
            return

        # print('prepare: ', index)
        if not is_full_white_image(res_img_arr):
            # print('sending yiedl: ', index)
            yield window, res_img_arr, index


def save_as_png(arr, label):
    img = Image.fromarray(arr, 'L')
    img.save(f'{label}.png')
