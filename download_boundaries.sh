#!/bin/sh

#downloads the boundary data for Loch Lomond and Cairngorms National Parks. Other UK national parks should have their data available on gov.uk too.

wget http://sedsh127.sedsh.gov.uk/Atom_data/ScotGov/ZippedShapefiles/SG_LochLomondTrossachsNationalPark_2002.zip
wget http://sedsh127.sedsh.gov.uk/Atom_data/ScotGov/ZippedShapefiles/SG_CairngormsNationalPark_2010.zip

unzip SG_LochLomondTrossachsNationalPark_2002.zip
unzip SG_CairngormsNationalPark_2010.zip

#Convert the shapefiles to a format GDAL can work with
#This solves the error:
#ValueError: shapefile must have lat/lon vertices  - it looks like this one has vertices in map projection coordinates. You can convert the shapefile to geographic coordinates using the shpproj utility from the shapelib tools

ogr2ogr -t_srs EPSG:4326 LochLomond.shp SG_LochLomondTrossachsNationalPark_2002.shp
ogr2ogr -t_srs EPSG:4326 Cairngorms.shp SG_CairngormsNationalPark_2010.shp

rm SG_LochLomondTrossachsNationalPark_2002*
rm SG_CairngormsNationalPark_2010*
