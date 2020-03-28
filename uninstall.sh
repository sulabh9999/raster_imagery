# !/bin/bash

# uninstall requirements
# pip3 uninstall --yes -r  requirements.txt

# # remove build, egg etc
# rm -rf build dist sdist *.egg-info

site_pkg_path=`python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])'`

find $site_pkg_path/ -iname "rtree*" -exec rm -rf {} \;
