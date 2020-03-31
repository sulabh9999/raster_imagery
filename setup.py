from setuptools import setup, find_packages
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'

install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='restro_imagery',
      version='1.0',
      description='Get all info of image in both command line and python API',
      license='MIT',
      author='Sulabh Shukla',
      author_email='sulabh9999@gmail.com',
      packages=find_packages(),
      download_url='https://github.com/sulabh9999/restro_imagery',
      maintainer_email='sulabh9999@gmail.com',
      install_requires=install_requires,
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Topic :: Software Development :: Build Tools'
      ],
      entry_points={'console_scripts': ['rim = rim.tools.main:main']},
      python_requires='>=3.6')
