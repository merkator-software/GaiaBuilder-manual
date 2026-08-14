# GaiaBuilder
ArcGIS Enterprise is often part of a large IT ecosystem. A DTAP is used for databases, applications and when GIS is part of it, also ArcGIS Enterprise or standalone ArcGIS Server. Manually administering the services in ArcGIS Enterprise this Developement, Test, Acceptance and Production street is time consuming and prone to errors. Furtermore, it is not integrated with the continuous deployment which is used for the GIS application consuming the services.
Integrating publishing the mapservices into the continuous deployment therefore has the following advantages:
* Better quality, because mapservices will be published exactly the same from the configuration
* Better performance, because it is very easy to perform an automated performance test every time you deploy a mapservice, making it easy to detect performance problems caused by a change in one of the layers
* Faster publishing, let the build server publish 4 mapservices in parallel, while you're working on something else
* Keep track of changes in the mapservices using Source Control Management (GIT or SVN)

GaiaBuilder helps you achieve better quality and faster publishing with a set of advanced Python scripts designed for ArcGIS Enterprise and ArcGIS Pro.  

The Item types in Portal Supported by GaiaBuilder:
- Mapservices using Enterprise geodatabase or file geodatabase
    - Featureservice extension
    - OGC extensions: WMS, WFS
    - ParcelFabricServer 
    - UtilityNetworkServer
    - ValidationServer
    - Vectortile service connected to the Featureservice
    - Scenelayers connected to the Featureservice
    - Custom SOE, SOI and Other extensions configurations
- Printservices using pagx layout templates
- Geoprocessing services created from .pyt toolboxes
- Locator services / Geocode services
- Image services
- Vectortile services using a Vectortile package (VTPK)
- Hosted Featureservices published via Service Definition File and with the data packages
- Hosted Featureservices published via REST, without the data but with data schema updates
- Hosted Featureservices published via REST, with a source FGDB in the Portal
- Web Maps
- Web Scenes
- Experience Builder applications
- Custom Experience Builder Widgets (Portal registration)
- Instant Apps
- Dashboards
- Storymaps
- Workflow Manager workflows
- Notebooks
- ArcGIS Enterprise Sites and Site Pages
- Documents (PDF, Excel) and Images as binary Files
- Zipped File Geodatabases and Zipped Shapefiles
- Registered third party services as Portal Items
- Services with stored Credentials (proxy services)
- Mobile Map Packages
- ArcGIS Pro Templates
- Vertigis Studio
    - Web applications
    - Workflows (client and server)
    - Report templates
    - Classic Print templates

Portal configurations supported by GaiaBuilder
- Groups
- Roles
- Portal Homepage and other resources




