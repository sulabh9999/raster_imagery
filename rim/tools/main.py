import argparse
import sys
import os
from importlib import import_module


def main():
    if not sys.version_info >= (3, 5):
        sys.exit("ERROR: raster imgery needs Python 3.5 or later.")

    tool_name = None
    if len(sys.argv) > 1:
        tool_name = sys.argv[1]

    assert tool_name, 'Please give tool name'

    parser = argparse.ArgumentParser(
        prog='rim',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='rastering satellite image and mask it with geojson')
    subparser = parser.add_subparsers(title="rim_tools")

    module = import_module(f'rim.tools.{tool_name}')
    module.add_parser(subparser)


if __name__ == '__main__':
    main()
