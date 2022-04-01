# Deploy a layer file to ArcGIS Enterprise
This example shows how a Layer file can be deployed to ArcGIS Enterprise

## Prerequisites
- An ArcGIS Pro APRX File with an empty map, which can be used to import the layer into. This file must be named Emptymap.aprx

## Relevant Properties
- lyrxjson : reference to a lyrx.json file in the same directory. This lyrx.json shouldn't contain a databaseconnectionstring and must be combined with the -l true (restore lyrx) and -k true (import lyrx) parameters on the commandline.
- lyrx : reference to a lyrx file. When combined with the lyrxjson property and -l commandline parameter, this file will be generated within the build. Otherwise, this file should be present in the same directory. The command line parameters must contain -k true (import lyrx).
- aprx : This file will be created from the Emptymap.aprx and the imported layer

## Command line parameters
- -l true : Set the -l parameter to true to instruct the build server to restore the databaseconnections from the .lyrx.json file to the .lyrx file
- -k true : Set the -k parameter to true to instruct the build server to import the layer into the Emptymap.aprx file.s