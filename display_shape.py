import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import cv2



def plot_shape(name):
    # create new figure, axes instances.
    fig=plt.figure()


    ax = fig.add_subplot(111)
    ax.axis("off")
    #convert the colour space of img 
    #ax.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

    #ax = fig.add_subplot(241)


    m = Basemap(llcrnrlon=-12.,llcrnrlat=49.5,urcrnrlon=2,urcrnrlat=59.5,rsphere=(6378137.00,6356752.3142),resolution='i',projection='merc',lat_0=40.,lon_0=-20.,lat_ts=20.)
    m.drawmapboundary(fill_color='#178fd1',linewidth='0.5')
    m.drawcoastlines()
    m.fillcontinents(color='#c9cbcc')

    m.readshapefile(name,'lochlomond');
    #make the national parks green
    patches   = []
    for shape in  m.lochlomond:
	patches.append( Polygon(np.array(shape), True) )

    ax.add_collection(PatchCollection(patches, facecolor= '#17d11d', edgecolor='k', linewidths=1., zorder=2))


    #m.plot(-4,52,latlon='True',color='m')

    plt.tight_layout()
    plt.savefig(name +".png")
    plt.close()


for i in range(0,14):
    plot_shape(str(i))
