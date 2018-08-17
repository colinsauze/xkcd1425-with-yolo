import shapefile
from shapely.geometry import shape, Point

#script to test a point inside every British national park

def get_park_name(lat, lon,parks, parknames):
    """Returns the name of the park this point is inside, parks is a list of park boundaries, parknames is their names"""
    
    point = Point(lon, lat)

    for i in range(len(parks)):
        polygon = parks[i]
        if polygon.contains(point):
            return parknames[i]



print parknames
print parks

test_points=[[51.75,-4.9],[52.8,-4],[52,-3.2],[51.2,-3.6],[50.5,-4],[50.8,-1.6],[51,-0.6],[52.6,1.6],[53.3,-1.7],[54.5,-3],[54.25,-2],[54.5,-1],[55,-2.5],[56.25,-4.5],[57,-4],[58,-4]]

for j in test_points:
    print("testing ",j[0],j[1])
    print(get_park_name(j[0],j[1],parks,parknames))
    print("")

