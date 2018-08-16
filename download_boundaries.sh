#!/bin/sh


wget "https://opendata.arcgis.com/datasets/df607d4ffa124cdca8317e3e63d45d78_1.zip?outSR=%7B%22wkid%22%3A27700%2C%22latestWkid%22%3A27700%7D" -O parks.zip

unzip parks.zip
ogr2ogr -t_srs EPSG:4326 UKParks.shp National_Parks_August_2016_Full_Extent_Boundaries_in_Great_Britain.shp
#split into individual parks
for i in `seq 0 15` ; do ogr2ogr -f "ESRI Shapefile" -dialect sqlite -sql "select * from UKParks limit 1 offset $i" $i.shp UKParks.shp ; done



#downloads the boundary data for Loch Lomond and Cairngorms National Parks. Other UK national parks should have their data available on gov.uk too.

wget http://sedsh127.sedsh.gov.uk/Atom_data/ScotGov/ZippedShapefiles/SG_LochLomondTrossachsNationalPark_2002.zip
wget http://sedsh127.sedsh.gov.uk/Atom_data/ScotGov/ZippedShapefiles/SG_CairngormsNationalPark_2010.zip

#Lake district
wget http://inspire.nationalparks.gov.uk/geoserver/ldnpa_inspire/ows?service=WFS&request=GetFeature&version=2.0.0&typeName=ldnpa_inspire:LDNPA_Boundary&outputFormat=shape-zip

wget http://balleter.nationalparks.gov.uk/geoserver/nymnpa_inspire/wms/kml?layers=nymnpa_inspire:nymnpa-npboundary

#welsh parks are in a different format
wget "https://gis.beacons-npa.gov.uk/geoserver/inspire/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=inspire:brecon_beacons_national_park_boundary&outputFormat=kml" -O brecon_beacons.kml



unzip SG_LochLomondTrossachsNationalPark_2002.zip
unzip SG_CairngormsNationalPark_2010.zip

#Convert the shapefiles to a format GDAL can work with
#This solves the error:
#ValueError: shapefile must have lat/lon vertices  - it looks like this one has vertices in map projection coordinates. You can convert the shapefile to geographic coordinates using the shpproj utility from the shapelib tools

ogr2ogr -t_srs EPSG:4326 LochLomond.shp SG_LochLomondTrossachsNationalPark_2002.shp
ogr2ogr -t_srs EPSG:4326 Cairngorms.shp SG_CairngormsNationalPark_2010.shp


ogr2ogr -t_srs EPSG:4326 BreconBeacons.shp brecon_beacons.kml 

rm SG_LochLomondTrossachsNationalPark_2002*
rm SG_CairngormsNationalPark_2010*
rm brecon_beacons.kml
