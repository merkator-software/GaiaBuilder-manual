# Deploy a mapservice with tile cache file to ArcGIS Enterprise
This example shows how a mapservice with a tile cache can be deployed to ArcGIS Enterprise.

See demo_cache.aprx.json for an example implementation

## Relevant Properties
- cachedirectory : the directory on the ArcGIS Server where the cache will be stored, this directory needs to be configured in ArcGIS Server Manager before it can be user here
- forcedeletetiles : optional, when set to true and a cache is present, the existing tiles will be deleted
- forcedeletecache : optional, when set to true and a cache is present, the cache will be removed, use this parameter to make changes to the tiling scheme. 
- forcecreatetiles : optional, when set to true, the all the cache tiles are generated 
- tilingscheme : json object containing the tiling scheme details

### tilingscheme properties
All properties below are required for the tiling scheme object
- numOfScales :  the number of scales in the tiling scheme
- scales :  the scales of the tiling scheme, must be an array with one or more numbers
- dots_per_inch : the dpi of the tiles, most often 96 dpi is used
- tileOrigin_x : the tiling scheme X origin 
- tileOrigin_y : the tiling scheme Y origin 
- tile_size :  the size in pixels of the tile images, options are: "128 x 128", "256 x 256","512 x 512","1024 x 1024"
- cache_tile_format :  the image format: options are: "PNG", "PNG8", "PNG24", "PNG32", "JPEG" and "MIXED" 
- tileCompressionQuality : the image compression for JPEG , possible values are 1-100, when one of the PNG formats is used, this value is ignored
- storage_format : "COMPACT" (Tiles will be grouped into large files called bundles. This storage format is efficient in terms of storage and mobility.)  or "EXPLODED" 
- update_extent :  "MAXOF" (The maximum extent of all inputs will be used.), "MINOF" (The minimum area common to all inputs will be used.) or a string with space delimited string of coordinates—The extent of the specified string will be used. Coordinates are expressed in the order of x-min, y-min, x-max, y-max.
- num_of_caching_service_instances : the number of caching instances used for generating or deleting cache tiles

## Command line parameters
- -t true : Set the -t parameter to true to instruct the build server create or update the mapservice tile cache
