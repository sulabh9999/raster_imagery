# rim tile
import os

# create a Polygon box to chip into training image and label
from shapely.geometry import box
from pyproj import CRS
import geopandas as gpd
from rasterio.features import rasterize
from rim.utils import (imageUtils, tiffUtils)
import rasterio

# others
from PIL import Image
import numpy as np
from tqdm import tqdm

#local
from constants import (DEFAULT_IMG_WINDOW, DEFAULT_STRIDE_WINDOW)


def rasterize(tif,
              geojson,
              out,
              size=DEFAULT_IMG_WINDOW,
              stride=DEFAULT_STRIDE_WINDOW):
    """
	start rasterizing tif file. here we have window with (args.size) and chunking tif image
	with size. this image are numpy array which is not stored in disk at this time. Geojson
	will be applyed on these image chunks with proper transformation for each polygone.

	chunks and masked images will be used as training dataset for Deep Learning model.
	tif image can be extra large, tools is able to handle it.

	Arg:
		tif - tif image path
		geojson - geojson file
		out - output directory
		size - size of window that user wants, default (h=512, w=512)  
		stride - stride size for sliding window, default same as window
	"""

    # read tif
    rst = rasterio.open(tif)

    # read geojson
    scene_labels_gdf = gpd.read_file(geojson)

    out_tif = os.path.join(out, 'tif')  # make tif dir
    out_mask = os.path.join(out, 'mask')  # make mask dir

    os.makedirs(out_tif, exist_ok=True)
    os.makedirs(out_mask, exist_ok=True)

    total = imageUtils.total_chunks_in_image(tif, window=size, stride=stride)

    with tqdm(total=total, desc='Masking progress') as pbar:
        # get image from sliding window
        for each in imageUtils.get_image_chunks(tif,
                                                window_size=size,
                                                stride=stride):

            # for win, arr in get_image_chunks(rst, window_size=(win_sz, win_sz)):
            img_window, img_arr, index = each[0], each[1], each[2]
            pbar.n = index
            pbar.refresh()

            # 'miny', 'maxx', and 'maxy'
            # (807592.8560103609, 620885.095643373, 807611.1959577247, 620903.4357975163)
            bounds = rasterio.windows.bounds(img_window, rst.meta['transform'])

            # shapely.geometry.polygon.Polygon for full image chunk (512, 512) in tiff
            win_box = box(*bounds)
            win_box_gdf = gpd.GeoDataFrame(geometry=[win_box],
                                           crs=rst.meta['crs'])
            win_box_gdf = win_box_gdf.to_crs(CRS.from_epsg(4326))

            try:
                # get chip from geopanda and bouning boxes with csr: 4326(Marcater)
                gdf_chip = gpd.sjoin(scene_labels_gdf,
                                     win_box_gdf,
                                     how='inner',
                                     op='intersects')
            except AttributeError as ae:
                pass

            # check if chip has data
            if not gdf_chip.empty:
                burn_val = 255
                shapes = [(geom, burn_val) for geom in gdf_chip.geometry]

                # transform
                chip_tfm = rasterio.transform.from_bounds(
                    *win_box_gdf.bounds.values[0], *size)
                label_arr = rasterio.features.rasterize(shapes,
                                                        out_shape=size,
                                                        transform=chip_tfm)

                img_tif_name = os.path.join(out_tif,
                                            str(index))  # make tif dir
                img_mask_name = os.path.join(out_mask,
                                             str(index))  # make mask dir

                # change dimension of chip image to save as tif
                win_arr = np.moveaxis(img_arr, 0, 2)
                tiffUtils.save_as_tif(win_arr,
                                      chip_tfm=chip_tfm,
                                      name=img_tif_name)

                # save mask image as png
                imageUtils.save_as_png(label_arr, img_mask_name)


def __validation(tif, geojson, out, size, stride):
    """	Validation for arguments and invoke function """
    # --tif
    if tif and not os.path.isfile(tif):
        raise ValueError(f"incorrect tif file: {tif}")

    # --geojson
    if geojson and not os.path.isfile(geojson):
        raise ValueError(f"incorrect geojson file: {geojson}")

    # --size
    try:
        size = tuple(map(int, size.split(","))) if size else (512, 512)
    except:
        raise ValueError("invalid --size for chunk")

    # --stride
    try:
        stride = tuple(map(int, stride.split(","))) if stride else (512, 512)
    except:
        raise ValueError("invalid --stride value")

    # --out
    if out and not os.path.exists(out):
        os.makedirs(out)

    return (tif, geojson, out, size, stride)


def add_parser(subparser):
    # print('args in subparser: ', args)
    parser = subparser.add_parser('tile_paser', help='parser for tile')

    inp = parser.add_argument_group("Inputs")
    inp.add_argument("--tif",
                     type=str,
                     required=True,
                     help="tif files to rasterize [required]")
    inp.add_argument("--geojson",
                     type=str,
                     required=True,
                     help="source geojson for ploting homes [required]")
    inp.add_argument("--size",
                     type=str,
                     default="512,512",
                     help="size of tile h,w default 512,512")
    inp.add_argument(
        "--stride",
        type=str,
        default=None,
        help=
        "Next jump when slidiing window horizontal and vertical (h,v) default is window size present in argument"
    )

    out = parser.add_argument_group("Output")
    out.add_argument("--out",
                     type=str,
                     required=True,
                     help="path to store tiles")

    parser.set_defaults(func=__main)
    args, unknown = parser.parse_known_args()

    args.func(args)


def __main(args):
    try:
        rasterize(*__validation(args.tif, args.geojson, args.out, args.size,
                                args.stride))
    except ValueError as ve:
        print('exception error here: ', ve)
