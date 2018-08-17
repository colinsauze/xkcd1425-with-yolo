#!/bin/sh


wget "https://opendata.arcgis.com/datasets/df607d4ffa124cdca8317e3e63d45d78_1.zip?outSR=%7B%22wkid%22%3A27700%2C%22latestWkid%22%3A27700%7D" -O parks.zip

unzip parks.zip
ogr2ogr -t_srs EPSG:4326 UKParks.shp National_Parks_August_2016_Full_Extent_Boundaries_in_Great_Britain.shp

rm parks.zip
rm National_Parks_August_2016_Full_Extent_Boundaries_in_Great_Britain.*
