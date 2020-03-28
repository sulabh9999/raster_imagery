# !/bin/bash

# 1. install .deb dependecny
cat deb_dependency.txt | xargs sudo apt-get install

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
