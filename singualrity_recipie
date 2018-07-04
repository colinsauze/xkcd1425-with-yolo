
Bootstrap:docker  
From:ubuntu:bionic

%labels
MAINTAINER Colin Sauze

%environment

%runscript
exec /bin/bash /bin/echo "Not supported"

%post  
apt-get install gdal-bin python-numpy python-opencv python-matplotlib python-matplotlib-data python-mpltoolkits.basemap python-mpltoolkits.basemap-data python-pil python-shapely 
git clone https://github.com/colinsauze/xkcd1425-with-yolo.git
cd xkcd1425-with-yolo
./setup.sh

