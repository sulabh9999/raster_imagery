# !/bin/bash

apt-get remove -y python3-rtree

# uninstall requirements
pip3 uninstall --yes -r  requirements.txt


# remove build, egg etc
rm -rf build dist sdist *.egg-info

# site_pkg_path=`python -c "import setuptools as st; print(st.__path__[0] + '/..')"`

# find $site_pkg_path/ -iname "rtree*" -exec rm -rf -- {} \;

