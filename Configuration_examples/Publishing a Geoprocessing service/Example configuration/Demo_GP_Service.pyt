# -*- coding: utf-8 -*-
					   

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the is the name of the class)."""
        self.label = "Basic Math Tools"
					  
        self.alias = "basicmath"
		# List of tool classes associated with this toolbox
        self.tools = [AddNumbers]

class AddNumbers(object):
						   


		   
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""										   
        self.label = "Add Two Numbers"
        self.description = "Adds two input numbers and prints the result"

    def getParameterInfo(self):
										 
        params = [
            arcpy.Parameter(
                displayName="First Number",
                name="first_number",
                datatype="GPDouble",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Second Number",
                name="second_number",
                datatype="GPDouble",
                parameterType="Required",
                direction="Input"
            )
        ]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""										  
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""		
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""																	   
																	  
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        a = parameters[0].value
        b = parameters[1].value
        result = a + b
        arcpy.AddMessage(f"🧮 The result of {a} + {b} is {result}")

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
								  
																  
								
			  
