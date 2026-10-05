# -*- coding: utf-8 -*-

import arcpy, os
from time import gmtime, strftime


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "DemoToolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "DemoTool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
        displayName="Content",
        name="content",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")

        param1 = arcpy.Parameter(
        displayName="Output file",
        name="DEFile",
        datatype="DEFile",
        parameterType="Optional",
        direction="Output")


        params = [param0, param1]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        content = parameters[0].valueAsText
        filepath =parameters[1].valueAsText
        if filepath is None or filepath =='':
            filename = strftime("%Y%m%d%H%M%S", gmtime()) + ".txt"
            filepath = os.path.join(arcpy.env.scratchFolder, filename )

        with open(filepath, 'w') as file:
            file.write('Your input was: ' + content)
        arcpy.SetParameterAsText(1,filepath)

        return
