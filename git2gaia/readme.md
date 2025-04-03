This Python script is provided as an alternative to the Powershell script for executing GaiaBuilder on the changed files in the repository

To run the script you need [GitPython](https://github.com/gitpython-developers/GitPython) for interaction with the GIT repository
Make sure you do a GIT checkout in your automation that allows a git diff, a shallow fetch might cause some issues there.

The script will execute the GIT diff, then analyze for each changed file what kind of work it is GaiaBuilder needs to do:
1. Publish Mapservices, hosted Featureservices with data, Imageservices, Scenelayers or ArcGIS Pro Template files
2. Publish Print or Geoprocessing services
3. Publish Portal content

GaiaBuilder will map this onto the GaiaBuilder JSON files and then proceed to execute GaiaBuilder for each of these files.

Place this python file within the GaiaBuilder installation directory

This file is provided as is and is not part of the GaiaBuilder solution. You're allowed to modify this file to meet your needs.  