# XKCD 1425 implementation with YOLO

!(https://imgs.xkcd.com/comics/tasks.png)

This code implements XKCD1425 by 

## Pre-requesites:

Python2

Python packages:

Numpy
OpenCV
Matplotlib/basemap
PIL
shapely
exif

System packages:
gdal-bin


### Setup:

running setup.sh will download the park boundary data, darknet and the yolo neural net weights. It will also compile darknet.

Currently only data for the two Scottish national parks are included. 

### Running:

> python2 detector.py

This will process all images in the test_images directory. It will write annotated images of the same name to the output_images directory. 
It also writes a CSV file summary to output_images/data.csv

### Example output:

(

