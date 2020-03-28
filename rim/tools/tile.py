import os

# create a Polygon box to chip into training image and label
from shapely.geometry import box
from pyproj import CRS
import geopandas as gpd
from rasterio.features import rasterize
from rim.utils import imageUtils 


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

    out = parser.add_argument_group("Output")
    out.add_argument("--out",
                     type=str,
                     required=True,
                     help="path to store tiles")

    parser.set_defaults(func=main)
    args, unknown = parser.parse_known_args()

    args.func(args)


def rasterize(args, stride=None):
    """
	start rasterizing tif file. here we have window with (args.size) and chunking tif image
	with size. this image are numpy array which is not stored in disk at this time. Geojson
	will be applyed on these image chunks with proper transformation for each polygone.

	chunks and masked images will be used as training dataset for Deep Learning model.
	tif image can be extra large, tools is able to handle it.
	"""
    scene_labels_gdf = gpd.read_file(args.geojson)

    img_list = [i for i in imageUtils.get_image_chunks(args.tif, window_size=args.size)]

    for index, each in enumerate(img_list[:20]):
        # for win, arr in get_image_chunks(rst, window_size=(win_sz, win_sz)):
        img_window, img_arr = each[0], each[1]

        # 'miny', 'maxx', and 'maxy'
        # (807592.8560103609, 620885.095643373, 807611.1959577247, 620903.4357975163)
        bounds = rasterio.windows.bounds(img_window, rst.meta['transform'])

        # shapely.geometry.polygon.Polygon for full image chunk (512, 512) in tiff
        win_box = box(*bounds)
        win_box_gdf = gpd.GeoDataFrame(geometry=[win_box], crs=rst.meta['crs'])
        win_box_gdf = win_box_gdf.to_crs(CRS.from_epsg(4326))

        gdf_chip = gpd.sjoin(scene_labels_gdf,
                             win_box_gdf,
                             how='inner',
                             op='intersects')

        if not gdf_chip.empty:
            burn_val = 255
            shapes = [(geom, burn_val) for geom in gdf_chip.geometry]

            chip_tfm = rasterio.transform.from_bounds(
                *win_box_gdf.bounds.values[0], win_sz, win_sz)
            label_arr = rasterize(shapes, (win_sz, win_sz), transform=chip_tfm)

            fig = plt.figure()

            win_arr = np.moveaxis(img_arr, 0, 2)
            ax1 = fig.add_subplot(1, 2, 1)
            ax1.imshow(win_arr)

            ax2 = fig.add_subplot(1, 2, 2)
            ax2.imshow(win_arr)

            ax1 = fig.add_subplot(1, 2, 2)
            ax1.imshow(label_arr, alpha=0.5)

            print(label_arr)
            break


def main(args):
    """
	Validation for arguments and invoke function
	"""
    # --tif
    if args.tif and not os.path.isfile(args.tif):
        raise ValueError(f"incorrect tif file: {args.tif}")

    # --geojson
    if args.geojson and not os.path.isfile(args.geojson):
        raise ValueError(f"incorrect geojson file: {args.geojson}")

    # --size
    try:
        args.size = tuple(map(int, args.size.split(",")))
    except:
        raise ValueError("invalid --size value, use --help")

    # --out
    if args.out and not os.path.exists(args.out):
        os.makedirs(args.out)

    # start rasterizing
    rasterize(args)
