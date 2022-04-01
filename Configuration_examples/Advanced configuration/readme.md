# Deploy a map file to ArcGIS Enterprise
This example shows some advanced configuration options for differentiating on Mapservice and FeatureService and for registering individual layers from the Mapservice and Featureservice as referenced layers and tables in Portal for ArcGIS. 

Registering the individual layers from a Mapservice or Featureservice makes the layers easy to find and use for your users. Especially when you created a Mapservice with a lot of layers, this can be helpful when a user only needs one layer from the service. Having registerMapserviceLayers+registerMapserviceTables and registerFeatureserviceLayers+registerFeatureserviceTables all active might result in a lot of layers and tables, because both the layer or table from the mapservice and the featureservice will be registered, it is adviced to choose either registerMapserviceLayers or registerFeatureserviceLayers

## Relevant Properties for registering individual layers
- registerMapserviceLayers : true or false, when set to true, all layers (except group layers) are registered with the url of the mapservice and the layerid (e.g.: Mapserver/0)
- registerMapserviceTables : true or false, when set to true, all tables are registered with the url of the mapservice and the tableid (e.g.: Mapserver/1)
- registerFeatureserviceLayers : true or false, when set to true, all layers (except group layers) are registered with the url of the mapservice and the tableid (e.g.: FeatureServer/0)
- registerFeatureserviceTables : true or false, when set to true, all tables are registered with the url of the mapservice and the tableid (e.g.: FeatureServer/1)
- layerTitleTemplate : template text which will be the title of the registered layer, placeholder {layerName} will be replaced with the actual layer name
- layerSnippetTemplate : template text which will be the summary of the registered layer, placeholder {layerName} will be replaced with the actual layer name
- layerDescriptionTemplate : template text which will be the description  of the registered layer, placeholder {layerName} will be replaced with the actual layer name, placeholder {dataset} will be replaced with the database table name and placeholder {definitionExpression} will be replaced with the applied definitionExpression on the layer

Please note that in this configuration, you need to define the tags, uselimitations and credits at the global level as well, because these properties are used to register the individual layers as well

## Relevant Properties for specific settings on the Mapservice or Featureservice
- FeatureService : Should contain a JSON object with one ore more of the following properties: tags, portaldescription, portalTitle, summary. These properties overwrite the default settings on the global level
- MapService : Should contain a JSON object with one ore more of the following properties: tags, portaldescription, portalTitle, summary. These properties overwrite the default settings on the global level


