# !/bin/bash

# 1. install .deb dependecny

# download c-library
apt-get install python3-rtree

# # extract 
# dpkg -x *.deb .pkg/

# # get python site-package path
# site_pkg_path=`python -c "import setuptools as st; print(st.__path__[0] + '/..')"`

# rsync -av .pkg/usr/lib/python3/dist-packages/* $site_pkg_path/
# # rm -rf /source/
# rm -rf *.deb .pkg


# 2. install setup
if [ ! -z "$1" ]
then
	# remove previous build files
	rm -rf build sdist *.egg-info

	case "$1" in 
  	"--dev") # install with --editable mode
		pip3 install -e .
		;;
	"--prod") # install with build mode
		# python3 setup.py install
		pip3 install .
		;;
	*) # incorrenct parameters
		echo "Sorry, I don't understand given parameters"
		;;
  esac
fi
