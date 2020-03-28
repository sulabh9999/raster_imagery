# !/bin/bash

# 1. install .deb dependecny

# download c-library
apt-get download python3-rtree

# mv *.deb .pkg/
# extract 
dpkg -x *.deb .pkg/

# # get python site-package path
site_pkg_path=`python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])'`

# #copy c-lib to site-package path
mv .pkg/usr/lib/python3/dist-packages/* $site_pkg_path/
rm -rf *.deb .pkg


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
