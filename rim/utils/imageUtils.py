import numpy as np
import collections
from rasterio.features import rasterize


# frame: (2353, 5674) image frame size (h, w)
# window_size: (512 512) size of window (h, w)
# stride: (10, 10) vertical and horizontal jump for each stride
def sliding_window(frame, window_size, stride=None):

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
    return np.mean(arr) == 0.0


def crop_center(np_img, crop_x, crop_y):
    y, x = np_img.shape
    startx = x // 2 - (crop_x // 2)
    starty = y // 2 - (crop_y // 2)
    return img[starty:starty + crop_y, startx:startx + crop_x]


def get_image_chunks(tif, window_size, stride=None, img_count=None):
    rst = rasterio.open(tif)

    res_height = rst.meta['height']
    res_width = rst.meta['width']

    for frame in sliding_window(frame=(res_height, res_width),
                                window_size=window_size,
                                stride=stride):
        window = Window(frame.x, frame.y, frame.width, frame.height)
        res_img_arr = rst.read(window=window)

        if not img_count:
            return None

        if not is_full_white_image(res_img_arr):
            img_count -= 1
            yield window, res_img_arr


# crop_center(img,4,6)
