from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import numpy as np
import cv2
#turn off X output, we just want to save a file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def make_map(lat,lon,img,outfilename):
    """Draws a map with a point at the given lat/lon onto image img and save it as outfilename"""
    
    # create new figure, axes instances.
    fig=plt.figure()

    ax = fig.add_subplot(111)
    ax.axis("off")
    #convert the colour space of img 
    ax.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

    ax = fig.add_subplot(241)
    # setup mercator map projection, centre it on scotland
    m = Basemap(llcrnrlon=-8.,llcrnrlat=54.5,urcrnrlon=-1,urcrnrlat=59.5,\
	        rsphere=(6378137.00,6356752.3142),\
    	    resolution='i',projection='merc',\
    	    lat_0=40.,lon_0=-20.,lat_ts=20.)
    
    #draw map boundaries and fill in colours
    m.drawmapboundary(fill_color='#178fd1',linewidth='0.5')
    m.drawcoastlines()
    m.fillcontinents(color='#c9cbcc')


    # draw parallels
    m.drawparallels(np.arange(10,90,1))
    # draw meridians
    m.drawmeridians(np.arange(-180,180,1))

    #draw the national parks
    m.drawcounties()
    m.readshapefile('LochLomond','lochlomond');
    m.readshapefile('Cairngorms','cairngorms');

    #make the national parks green
    patches   = []
    for shape in  m.cairngorms:
	patches.append( Polygon(np.array(shape), True) )

    for shape in  m.lochlomond:
	patches.append( Polygon(np.array(shape), True) )

    ax.add_collection(PatchCollection(patches, facecolor= '#17d11d', edgecolor='k', linewidths=1., zorder=2))

    #plot/save the map
    m.plot(lon,lat, latlon='True',marker='o',color='m')

    plt.tight_layout()
    plt.savefig(outfilename)
    plt.close()