# rim - raster imgery

Split large spatial image(GeoTIFF) into small chips and mask it with associated geojson.

[![](https://img.shields.io/badge/python-3.5%7C3.6%7C3.7-brightgreen)]() [![](https://img.shields.io/badge/spatial-imagery-orange)]() [![](https://img.shields.io/badge/Tiff-geojson-brightgreen)]() 

Geographic information systems use GeoTIFF and other formats to organize and store gridded, or raster, datasets. Raster-imagery reads and splits into chunks with masked data called GeoJson, and provides a Python API and command line tool.

![](https://i.ibb.co/TKBny0n/1935.png) ![](https://i.ibb.co/9YqY1w3/1935.png)

### Prerequisites

basic requirements are

```
c-library libspatialindex
python >= 3.5
virtualenv
```

### Installing

Setup virtualenv

```
virtualenv --python=python3.5 venv
source venv/bin.activate
```

#### general installation
```
sudo apt-get install python3-rtree
git clone https://github.com/sulabh9999/raster_imagery.git
cd raster_imagery
pip3 install .
```
#### auto  installation
```
git clone https://github.com/sulabh9999/raster_imagery.git
cd raster_imagery
sudo sh install.sh --build 
```


## Examples

Here's an example of some basic features that raster-imagery provides.

### command line tools

```
# with default window size and stride
rim tile \
	--tiff example.tif \
	--geojson example.geojson
	
# when size is given
rim tile \
	--tiff example.tif \ 
	--geojson example.geojson \
	--size 1024,1024 \
	--stride 100,100
```

### python code

Explain how to use python API

```
import rim.tools.tile as rt

tif = 'example.tif'
geojson = 'example.geojson'
window_size = (1024, 1024) # default (512, 512)
stride = (100, 100) # default (512, 512)
out = '/path/for/output/dir'
rt.rasterize(tif=tif, geojson=geojson, out=out, size=window_size, stride=stride)
```

## Contributing

Please read [CONTRIBUTING.md](https://github.com/sulabh9999/raster_imagery/blob/master/CONTRIBUTING.md)  for submitting pull requests to us.

## Version

version 1.0
## Authors

* **Sulabh Shukla** - *Initial work* - [Open source contributer, Ex-DBS](https://github.com/sulabh9999)
* **Nikhil Mahen** - *Initial work* - [CEO at Releaf Today, Ex-DBS](https://github.com/PurpleBooth)

## TODO

* Need to split spatical image for other formats like png, jpeg, webP, etc.
* Need to add threading enviromnent to speed up process.
* Need to add WGS84 Marcater projection for tileing.

See also the list of [contributors](https://github.com/sulabh9999/raster_imagery/blob/master/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE]() file for details

