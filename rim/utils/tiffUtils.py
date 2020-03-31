import rasterio


def save_as_tif(arr, chip_tfm, name='test', crs='EPSG:4326', dtype='uint8'):
    im = (arr).astype(dtype)

    # check im shape, number of channels and expand into (H,W,C) if needed
    if len(im.shape) == 3:
        num_ch = im.shape[-1]
    else:
        num_ch = 1
        im = np.expand_dims(im, -1)

    with rasterio.open(f'{name}.tif',
                       'w',
                       driver='GTiff',
                       height=im.shape[0],
                       width=im.shape[1],
                       count=num_ch,
                       dtype=im.dtype,
                       crs=crs,
                       transform=chip_tfm,
                       compress='LZW') as dst:

        for ch in range(num_ch):
            dst.write(im[:, :, ch], indexes=ch + 1)
