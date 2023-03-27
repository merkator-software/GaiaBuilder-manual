# Multple mapservices from one repository
The Git-intelligent-pipeline contains a Powershell script which detects the changes and publishes only the mapservices from the changed files. Combined with the trigger on the develop branch in this example, the pipeline automatically runs and publishes the changed files.

To make this work, a file name convention needs to be applied:
* There cannot be a . (dot) character in the first part of the filename. For example: mymapservice.aprx.json or mymapservice.maps.json is fine, but my.mapservice.aprx.json or my.mapservice.mapx.json might result in erros.
* The ArcGIS Pro file (\*.lyrx.json, \*.lyrx, \*.mapx.json, \*.mapx)  and GaiaBuilder configuration file (\*.aprx.json) must share the first part of the file name \*. For example, if you created mymapservice.mapx.json, the powershell script expects a mymapservice.aprx.json file.
