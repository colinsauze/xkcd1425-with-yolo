# XKCD 1425 implementation with YOLO

![XKCD1425 cartoon](https://imgs.xkcd.com/comics/tasks.png)

This code automatically determines if an image was taken in a national park and if it contains any birds. It implements the scenario shown in the XKCD comic number 1425. It uses the [YOLO image classifier](https://pjreddie.com/darknet/yolo/) and the [Darknet](https://pjreddie.com/darkne) neural network framework to do the bird detection. This has been trained on the [COCO dataset](http://cocodataset.org/). Currently it only works with the two national parks in Scotland (Loch Lomond & the Trossachs National Park and Cairngorms National Park) although more could easily be added. 

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

![example image 1](https://raw.githubusercontent.com/colinsauze/xkcd1425-with-yolo/master/output_images/Duck2.jpg)
![example image 2](https://raw.githubusercontent.com/colinsauze/xkcd1425-with-yolo/master/output_images/Seagulls.jpg)
![example image 3](https://raw.githubusercontent.com/colinsauze/xkcd1425-with-yolo/master/output_images/Train.jpg)

