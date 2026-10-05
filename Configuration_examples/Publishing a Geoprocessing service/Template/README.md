Template: Publishing a Geoprocessing service
=======================
> **Note:** Throughout this document, the term **GeoProcessing** will be abbreviated as **GP**.

This folder is a starting point for deploying a new GP service with GaiaBuilder. Copy this folder for every new GP service, then work through the files below. See the [Example configuration](../Example%20configuration) for a filled-in reference, and [Publish a Geoprocessing service](../README.md) for the full step-by-step walkthrough.

### Files in this template
* `demo_toolbox.pyt`, `demo_toolbox.pyt.xml`, `demo_toolbox.Tool.pyt.xml`: the Python toolbox and its metadata, replace these with your own toolbox, tool and metadata XML files
* `stage.py`: modify the `runTheTool` function to import your toolbox and call your GP tool with representative parameters, the rest of the file should not be modified
* `gpservice.json`: the GP service deploy configuration, see below for which properties to change
* `server.json`: not included in this template, create it yourself as described in [Publish a Geoprocessing service](../README.md), it configures the server folder, portal folder, data sources and sharing per environment
* `__init__.py`: leave this file as is, it's required for the toolbox to be importable

### Properties to change in gpservice.json
Replace these for every new GP service:
* `toolbox`: the filename of your toolbox .pyt file
* `name`: the service name. On a Virtual DTAP, where multiple environments share the same ArcGIS Server, suffix it with the environment it's published to by convention, e.g. `_DEV`, to keep the name unique and matching the environment configured in `serverFolder`. This isn't needed when each environment is a different physical stage
* `serverFolder`: the ArcGIS Server folder this environment's version of the service is published to
* `portalFolder`: the Portal folder this environment's version of the service is published to
* `description`, `summary`, `tags`, `uselimitations`, `credits`: replace the placeholder text with information describing your own service
* `portalLogo`: either add your own thumbnail image to this folder and update this property to its filename, or remove the property if you don't want a logo
* `categories`: optional, add the content categories configured in your Portal, or leave the array empty
* `targetitemid`: optional, not present in this template by default. Set it to a hardcoded 32 character hexadecimal ItemID to apply the exact same ItemID across every environment, or set it to an empty string to have GaiaBuilder generate the ItemID from a MD5 hash of the URL subfolder instead. Leaving the property out entirely assigns a random ItemID

Usually left unchanged:
* `action`, `stageScript`, `serviceType`: required constants
* `serverconfiguration`: keep pointing at `server.json`, unless you rename that file
* `content_status`, `protected`, `executionType`, `copyData`, `maxIdleTime`, `maxInstancesPerNode`, `maxStartupTime`, `maxUsageTime`, `maxWaitTime`, `minInstancesPerNode`, `recycleInterval`, `recycleStartTime`: sensible defaults, only tune these if your service needs different resource or performance settings

For an overview of every available property, see the [GP JSON configuration](https://github.com/merkator-software/GaiaBuilder-manual/wiki/GP-JSON-configuration) reference.
