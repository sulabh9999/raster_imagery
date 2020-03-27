import argparse
import sys
import os
from importlib import import_module


def main():
	if not sys.version_info >= (3, 5):
		sys.exit("ERROR: raster imgery needs Python 3.5 or later.")

	tool_name = sys.argv[1]

	parser = argparse.ArgumentParser(prog='rim', formatter_class=argparse.RawDescriptionHelpFormatter, description='rastering satellite image and mask it with geojson')
	subparser = parser.add_subparsers(title="rim_tools")

	module = import_module(f'rim.tools.{tool_name}')
	module.add_parser(subparser)

	# args = parser.parse_args()
	# tile_parser = subparser.add_parser('tile parser', help='parser for tile')

	# # s = tile_parser.parse_args()
	# # print('args in main--: ', s)

	# inp = tile_parser.add_argument_group("Inputs")
	# inp.add_argument("--tiff", type=str, required=True, help="tif files to rasterize [required]")
	# #
	# args = parser.parse_args()
	# print('args in main: ', parser.parse_args().tool)









# def main():
# 	if not sys.version_info >= (3, 5):
# 		sys.exit("ERROR: raster imgery needs Python 3.5 or later.")


# 	parser = argparse.ArgumentParser(prog='rim', description='rastering satellite image and mask it with geojson')
# 	# parser.add_argument('tool', help='Name of an image')
# 	subparser = parser.add_subparsers(title="rim_tools")

# 	# args = parser.parse_args()
# 	tile_parser = subparser.add_parser("tile")

# 	# s = tile_parser.parse_args()
# 	# print('args in main--: ', s.tile)

# 	inp = tile_parser.add_argument_group("Inputs")
# 	inp.add_argument("--tiff", type=str, required=True, help="tif files to rasterize [required]")
# 	#
# 	args = parser.parse_args()
# 	print('args in main: ', args.tile)
# 	# args.func(args) 
# 	# print(args)

# 	# module = import_module("rim.tools.{}".format(args.tool))
# 	# module.add_parser(subparser)

# 	# print(args)

# 	# try:
# 	# 	args.func(args)
# 	# except Exception as error:
# 	# 	parser.print_help()
# 	# 	parser.exit("{} ARG PARSER ERROR: {}".format(os.linesep, error))
			
if __name__ == '__main__':
	main()
