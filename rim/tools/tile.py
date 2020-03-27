import os

# create a Polygon box to chip into training image and label 
from shapely.geometry import box
from pyproj import CRS
import geopandas as gpd
from rasterio.features import rasterize


def add_parser(subparser):

	# print('args in subparser: ', args)
	parser = subparser.add_parser('tile_paser', help='parser for tile')

	inp = parser.add_argument_group("Inputs")
	inp.add_argument("--tiff", type=str, required=True, help="tif files to rasterize [required]")
	inp.add_argument("--geojson", type=str, required=True, help="source geojson for ploting homes [required]")
	inp.add_argument("--size", type=str, default="512,512", help="size of tile (h, w) [required]")
	
	out = parser.add_argument_group("Output")
	out.add_argument("--out", type=str, required=True, help="path to store tiles")

	args, unknown = parser.parse_known_args()

	parser.set_defaults(func=main)
	print('args in main: ', args)

	# args.func(args)






	# ================
	# parser = subparser.add_parser("tile", help="Helps to create tiles")

	# inp = parser.add_argument_group("Inputs")
	# inp.add_argument("--tiff", type=str, required=True, default=None, nargs='+', help="tif files to rasterize [required]")
	# # inp.add_argument("--geojson", type=str, required=True, help="source geojson for ploting homes [required]")
	# # inp.add_argument("--size", type=str, default="512,512", help="size of tile (h, w) [required]")
	
	# # out = parser.add_argument_group("Output")
	# # out.add_argument("--out", type=str, required=True, help="path to store tiles")

	# # print('parser: ', parser)
	# parser.set_defaults(func=main)
	# # main(parser)
	# args = parser.parse_args()
	# args.func(args)


def rasterize(tif, geojson, window_size, stride=None):
	img_arr = None
	img_window = None

	scene_labels_gdf = gpd.read_file(geojson)	

	img_list = [i for i in get_image_chunks(rst, window_size=window_size, img_count=100)]

	for index, each in enumerate(img_list[:20]):
		# index = 8
		# for win, arr in get_image_chunks(rst, window_size=(win_sz, win_sz)):
		img_window, img_arr = each[0], each[1] #img_list[index][0], img_list[index][1]

		win_arr = np.moveaxis(img_arr,0,2)
		# plt.figure(figsize=(5,5))
		# plt.imshow(win_arr)



		# 'miny', 'maxx', and 'maxy'
		# (807592.8560103609, 620885.095643373, 807611.1959577247, 620903.4357975163)
		bounds = rasterio.windows.bounds(img_window, rst.meta['transform'])

		# shapely.geometry.polygon.Polygon for full image chunk (512, 512) in tiff
		win_box = box(*bounds)
		win_box_gdf = gpd.GeoDataFrame(geometry=[win_box], crs=rst.meta['crs'])
		win_box_gdf = win_box_gdf.to_crs(CRS.from_epsg(4326))


		gdf_chip = gpd.sjoin(scene_labels_gdf, win_box_gdf, how='inner', op='intersects')
		# print(gdf_chip)

		if not gdf_chip.empty:
			burn_val = 255
			shapes = [(geom, burn_val) for geom in gdf_chip.geometry]
			shapes[0][0]

			chip_tfm = rasterio.transform.from_bounds(*win_box_gdf.bounds.values[0], win_sz, win_sz)
			label_arr = rasterize(shapes, (win_sz, win_sz), transform=chip_tfm)

			fig = plt.figure()

			ax1 = fig.add_subplot(1,2,1)
			ax1.imshow(win_arr)

			ax2 = fig.add_subplot(1,2,2)
			ax2.imshow(win_arr)

			ax1 = fig.add_subplot(1,2,2)
			ax1.imshow(label_arr, alpha=0.5)

			print(label_arr.shape)
			break





def main(args):

	print('i am in main in tile', args)

	# if args.tif and not os.path.exist(args.tif):
	# 	raise ValueError("Doesn't exist --tiff file")

    # try:
    #     args.size = list(map(int, args.bands.split(","))) if args.bands else None
    # except:
    #     raise ValueError("invalid --args.bands value")

    # try:
    #     args.bands = list(map(int, args.bands.split(","))) if args.bands else None
    # except:
    #     raise ValueError("invalid --args.bands value")

    # try:
    #     args.bands = list(map(int, args.bands.split(","))) if args.bands else None
    # except:
    #     raise ValueError("invalid --args.bands value")


	# rasterize(args.tif, arg.geojson, args.window_size)
	

	
