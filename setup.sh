#!/bin/sh

#get park boundary data
./download_boundaries.sh

git submodule update --init --recursive
cd darknet
make
#commented out for test mode
#wget https://pjreddie.com/media/files/yolov3.weights
cd ..

#annoying hack to make sed replace the path
libdarknet=`pwd`"/darknet/libdarknet.so"
echo $libdarknet | sed 's/\//\\\//g' > libdarknet.path
libdarknet=`cat libdarknet.path` 
rm libdarknet.path

sed -i "s/libdarknet.so/$libdarknet/" darknet/python/darknet.py 

sed -i 's/data\/coco.names/darknet\/data\/coco.names/' darknet/cfg/coco.data 



