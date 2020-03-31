# rim - raster imagery

Split large spatial image(GeoTIFF) into small chips and mask it with associated geojson.

[![](https://img.shields.io/badge/python-3.5%7C3.6%7C3.7-brightgreen)]() [![](https://img.shields.io/badge/spatial-imagery-orange)]() [![](https://img.shields.io/badge/Tiff-geojson-brightgreen)]() 

Geographic information systems use GeoTIFF and other formats to organise and store gridded, or raster, datasets. Raster-imagery reads and splits into chunks with masked data called GeoJson, and provides a Python API and command line tool.


<img src="https://i.ibb.co/TKBny0n/1935.pngg" width="300"/> <img src="https://i.ibb.co/9YqY1w3/1935.png" width="300"/>

### Prerequisites

basic requirements are


libspatialindex - c++ level library</br>
python >= 3.5</br>
virtualenv==15.1.0</br>
pip3 ==20.0.2


### Installing

Setup virtualenv

```sh
virtualenv --python=python3.5 venv
source venv/bin/activate
```

#### general installation
```sh
sudo apt-get install python3-rtree
git clone https://github.com/sulabh9999/raster_imagery.git
cd raster_imagery
pip3 install .
```
#### auto  installation
```sh
git clone https://github.com/sulabh9999/raster_imagery.git
cd raster_imagery
sudo sh install.sh --build 
```


## Examples

Here's an example of some basic features that raster-imagery provides.

### command line tools

```sh
# with default window size and stride
rim tile \
	--tiff example.tif \
	--geojson example.geojson \
	--out='output_dir'
	
# when size is given
rim tile \
	--tiff example.tif \
	--geojson example.geojson \
	--out='output_dir' \
	--size 1024,1024 \
	--stride 100,100
```

<a href="https://ibb.co/Wy017Rv"><img src="https://i.ibb.co/swCrcX9/Screenshot-from-2020-03-30-22-59-44.png" alt="Screenshot-from-2020-03-30-22-59-44" border="0"></a>

### python code

Explain how to use python API

```python
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

* [Sulabh Shukla](https://in.linkedin.com/in/sulabh-shukla-8a675794) - *Initial work* - [Open source contributer](https://github.com/sulabh9999), [Ex-DBS](https://www.dbs.com/in/index/default.page)
* [Nikhil Mahen](https://in.linkedin.com/in/nikhil-mahen-50149b10) - *Initial work* - [CEO at Releaf Today, Ex-DBS](https://in.linkedin.com/in/nikhil-mahen-50149b10)

## TODO

* Split spatial image for other formats such as png, jpeg, webP, etc.
* Threading environment to speed up process.
* WGS84 Marcater projection for tiling.
* Masking for other labels such as road, rivers, trees, vehicles etc.

See also the list of [contributors](https://github.com/sulabh9999/raster_imagery/blob/master/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE]() file for details

## other links
- [open city challenge](https://www.drivendata.org/competitions/60/building-segmentation-disaster-resilience/)
- [OSM](https://www.openstreetmap.org/#map=4/21.84/82.79)
