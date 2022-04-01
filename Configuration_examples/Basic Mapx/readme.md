# Deploy a map file to ArcGIS Enterprise
This example shows how a Map file can be deployed to ArcGIS Enterprise

## Prerequisites
- An ArcGIS Pro APRX File without any content, which can be used to import the map into. This file must be named blank.aprx

## Relevant Properties
- mapxjson : reference to a mapx.json file in the same directory. This mapx.json shouldn't contain databaseconnectionstrings for the layers or tables and must be combined with the -q true (restore mapx) and -m true (import mapx) parameters on the commandline.
- mapx : reference to a mapx file. When combined with the mapxjson property and -l commandline parameter, this file will be generated within the build. Otherwise, this file should be present in the same directory. The command line parameters must contain -k true (import mapx).
- aprx : This file will be created from the Emptymap.aprx and the imported layer

## Command line parameters
- -q true : Set the -q parameter to true to instruct the build server to restore the databaseconnections from the .mapx.json file to the .mapx file
- -m true : Set the -m parameter to true to instruct the build server to import the layer into the Emptymap.aprx file.