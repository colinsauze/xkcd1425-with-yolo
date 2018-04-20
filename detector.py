# Stupid python path shit.
# Instead just add darknet.py to somewhere in your python path
# OK actually that might not be a great idea, idk, work in progress
# Use at your own risk. or don't, i don't care

import sys, os
sys.path.append(os.path.join(os.getcwd(),'python/'))

import darknet as dn
import pdb

import json
import cv2

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

from map import make_map

from exif import get_exif_data, get_lat_lon

import shapefile
from shapely.geometry import shape, Point



#convert shapefiles
#ValueError: shapefile must have lat/lon vertices  - it looks like this one has vertices in map projection coordinates. You can convert the shapefile to geographic coordinates using the shpproj utility from the shapelib tools
#ogr2ogr -t_srs EPSG:4326 LochLomond.shp SG_LochLomondTrossachsNationalPark_2002.shp
#ogr2ogr -t_srs EPSG:4326 Cairngorms.shp SG_CairngormsNationalPark_2010.shp


def get_park_name(lat, lon,parks, parknames):
    """Returns the name of the park this point is inside, parks is a list of park boundaries, parknames is their names"""
    
    point = Point(lon, lat)

    for i in range(len(parks)):
        polygon = parks[i]
        if polygon.contains(point):
            return parknames[i]            


#from https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv/14102014#14102014
def overlay_image(x_offset,y_offset,overlay,target):
    """Overlay one OpenCV image on top of another. x_offset and y_offset are the location of the top corner of the image being overlaid. overlay is the image to overlay, and target is the target image to draw overlay onto."""
    y1, y2 = y_offset, y_offset + overlay.shape[0]
    x1, x2 = x_offset, x_offset + overlay.shape[1]

    alpha_s = overlay[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        target[y1:y2, x1:x2, c] = (alpha_s * overlay[:, :, c] + alpha_l * target[y1:y2, x1:x2, c])
        
    #target[y_offset:y_offset+overlay.shape[0], x_offset:x_offset+overlay.shape[1]] = overlay         


def findbirds(target_dir,output_dir):

    #build a list of park boundaries
    parks = [0,0]
    # read the shapefiles
    parks[0]= shape(shapefile.Reader("Cairngorms.shp").shapes()[0])
    parks[1]= shape(shapefile.Reader("LochLomond.shp").shapes()[0])
    #store the park names
    parknames = [ "Cairngorms", "Loch Lomond"]

    #darknet setup
    dn.set_gpu(0)
    #download yolov3.weights from  https://pjreddie.com/media/files/yolov3.weights
    net = dn.load_net("cfg/yolov3.cfg", "yolov3.weights", 0)
    meta = dn.load_meta("cfg/coco.data")

    #list of extensions to process 
    extensions=('.jpeg','.jpg')

    font = cv2.FONT_HERSHEY_DUPLEX

    tick_img = cv2.imread("tick.png", -1)
    cross_img = cv2.imread("cross.png", -1)
    csvfile = open(output_dir+'/data.csv','w')
    csvfile.write("\"Filename\",\"Latitude\",\"longitude\",\"Park Name\",\"Bird\"\n")

    #loop through all the image files in the target directory
    for subdir, dirs, files in os.walk(target_dir):
        print files
        for file in files:
            
            #only process extensions we're interested in
            fullfile=target_dir+"/"+file
            ext = os.path.splitext(fullfile)[-1].lower()
            
            
            if ext in extensions:
                print "Processing image " + file
                image = Image.open(fullfile)
                #get JPEG Exif header to find the GPS coordinates of the image
                exif_data = get_exif_data(image)
                image.close()
                lat_lon = get_lat_lon(exif_data)
                
                if lat_lon[0] is None:
                    print file + " has no geolocation data"
                    continue
                
                lat=lat_lon[0]
                lon=lat_lon[1]
                parkname=get_park_name(lat,lon,parks,parknames)
                
                #load the image and run the darknet/yolo detector on it
                im = cv2.imread(fullfile)
                r = dn.detect(net,meta,fullfile)
                birdfound = 0
                
                #loop through all the objects found by darknet
                for obj in r:
                    objclass=str(obj[0])
                    if objclass == "bird":
                        birdfound=1
                        
                        #get the image bounding box
                        x=int(obj[2][0])
                        y=int(obj[2][1])
                        h=int(obj[2][3])
                        w=int(obj[2][2])

                        x=x-(w/2)
                        y=y-(h/2)
                        cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),4)
                        cv2.putText(im,str(obj[0]),(x,y-10),font,2,(0,255,0),2)

                #draw the text in black and white with slight offsets between them
                #this makes it readable whether there's a dark or light area under it
                cv2.putText(im,"Bird:",(850,150),font,3,(255,255,255),2)                                   
                cv2.putText(im,"Bird:",(854,154),font,3,(0,0,0),2)            

                #display tick/cross images depending on whether the image has a bird
                #and was taken in a park or not
                if birdfound==1:
                    overlay_image(1100,80,tick_img,im)
                
                else:
                    overlay_image(1100,80,cross_img,im)               

                cv2.putText(im,"Park:",(1500,150),font,3,(255,255,255),2)
                cv2.putText(im,"Park:",(1504,154),font,3,(0,0,0),2)
                    
                if parkname is None:
                    overlay_image(1800,80,cross_img,im)
                    parkname="none"
                    
                else:
                    overlay_image(1800,80,tick_img,im)                

                #resize output file so its not so big
                small = cv2.resize(im, (0,0), fx=0.35, fy=0.35) 
                
                #draw the map of the geolocation onto the image
                make_map(lat,lon,small,output_dir+"/"+file)
                
                #save output to a CSV file
                csvfile.write("\"%s\",%f,%f,%s,%d\n" % (fullfile,lat,lon,parkname,birdfound))
                            

    csvfile.close()

findbirds(target_dir="test_images",output_dir="output_images")