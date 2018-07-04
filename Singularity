Bootstrap:docker  
From:ubuntu:bionic

%help
    Container for XKCD 1424 with Yolo demo. 
    To install run: 
	sudo singularity build xkcd1425.img Singularity
    To run (replace /home/user/output_images with the directory where you want the output and /home/user/input_images with the directory containing the images you want to process)
	singularity run -B /home/user/input_images:/opt/xkcd1425-with-yolo/test_images,/home/user/output_images:/opt/xkcd1425-with-yolo/output_images xkcd1425.img

%labels
    MAINTAINER Colin Sauze

%environment


%post  
    pwd
    apt-get update
    apt-get -y install unzip wget build-essential git gdal-bin python-numpy python-opencv python-matplotlib python-matplotlib-data python-mpltoolkits.basemap python-mpltoolkits.basemap-data python-pil python-shapely 

    cd /opt
    git clone https://github.com/colinsauze/xkcd1425-with-yolo.git
    cd xkcd1425-with-yolo
    ./setup.sh

    #remove the example images so we can write new ones
    #uncomment if you want to process the example images in the git repo, output will be saved in the container and then lost
    #chmod 777 output_images
    #rm output_images/*

%runscript
    cd /opt/xkcd1425-with-yolo
    python detector.py 
