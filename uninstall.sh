# !/bin/bash

# get records
# python setup.py install --record files.txt

# # remove dependencies
# cat files.txt | xargs rm -rf

# # remove cache
# rm files.txt

# uninstall requirements
pip3 uninstall --yes -r  requirements.txt

# remove build, egg etc
rm -rf build dist sdist *.egg-info
