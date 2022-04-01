# Deploy a map file to ArcGIS Enterprise
This example shows how you can configure to use metadata from a EGDB Layer. The metadata will be read from the database when published and used to configure the title, summary, description, tags and use limitations*. 

## Prerequisites
- A .Mapx.json, .Mapx, .lyrx.json or .lyrx file with one layer with metadata configured in the database. Connect to the database using an .sde file, right click the layer and choose edit metadata from the context menu to add metadata to the layer.
[[example.png]]

## Relevant Properties
- metadatafromlayer": "true", : Set this parameter to "true" to read the metadata from the database. The first layer which can contain metadata and which has metadata will be used. In case no layers with metadata are found, a warning is written to the log file

Don't use the properties below when the metadata should come from the database. Setting these properties in the JSON overrules the configuration from the database metadata
- summary 
- portalTitle
- portaldescription 
- tags 
- credits 
- uselimitations 

*Setting the thumbnail from the metadata in the database is currently not possible, this feature will become available in a future release.

