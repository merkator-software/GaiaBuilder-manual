#-------------------------------------------------------------------------------
# Name:        InstallMapserviceTool
# Purpose:     Example code running a custom tool, staging and publishing
#
# Author:      Merkator B.V.
#
# Created:     10-05-2020
# Copyright:   Merkator B.V.
#-------------------------------------------------------------------------------
import arcpy, sys, getopt, os
import xml.dom.minidom as DOM

#modify this function to run your toolbox
def runTheTool(toolbox):
    # Import the toolbox with the 'basicmath' alias
    arcpy.ImportToolbox(toolbox, 'basicmath')
    
    # List to store results
    results = []
    
    # Run AddNumbers tool with valid inputs (1 + 2)
    try:
        add_result = arcpy.basicmath.AddNumbers(1, 2)
        results.append(add_result)
        arcpy.AddMessage(f"AddNumbers result: {add_result}")
    except Exception as e:
        arcpy.AddError(f"AddNumbers failed: {str(e)}")
    
    # Run DivideNumbers tool with valid inputs (10 ÷ 2)
    try:
        div_result = arcpy.basicmath.DivideNumbers(10, 2)
        results.append(div_result)
        arcpy.AddMessage(f"DivideNumbers result: {div_result}")
    except Exception as e:
        arcpy.AddError(f"DivideNumbers failed: {str(e)}")
    
    return results


#do not modify code below
def prepdir(workdir, draftsdir ,sddraft ,sd):
    if not os.path.isdir(workdir):
        os.mkdir(workdir)
    if not os.path.isdir(draftsdir):
        os.mkdir(draftsdir)

    if os.path.isfile(sddraft):
        os.remove(sddraft)
    if os.path.isfile(sd):
        os.remove(sd)


def stageFederated(portalurl, portalusername, portalpassword, result, serverURL, serviceName,servicefolder,  workdir, executionType, copydata, connection_file_path, stage, publish, overwrite , summary, tags, jobdir, outputdir):
    draftsdir = os.path.join(workdir,"drafts")

    sddraft = os.path.join( draftsdir,serviceName + ".sddraft")
    fixedsddraft = os.path.join( draftsdir,serviceName + "fixed.sddraft")
    sd =os.path.join(workdir, serviceName+ ".sd")

    if stage:
        prepdir(workdir, draftsdir ,sddraft ,sd)

        server_type = 'MY_HOSTED_SERVICES'
        if connection_file_path is not None:
            server_type = "FROM_CONNECTION_FILE"

        # Sign in Portal if username and password are provided, if none are supplied, it is assumed arcpy is succesfully signed in elsewhere
        if portalusername is not None and portalpassword is not None: 
            arcpy.SignInToPortal(portalurl, portalusername, portalpassword)

        # Create service definition draft and return analyzer messages
        analyzeMessages = arcpy.CreateGPSDDraft(
            result, sddraft, serviceName, server_type=server_type,connection_file_path = connection_file_path,
            copy_data_to_server=copydata, folder_name=servicefolder,
            summary=summary, tags=tags, executionType=executionType,
            resultMapServer=False, showMessages="INFO", maximumRecords=5000,
            minInstances=1, maxInstances=1, maxUsageTime=100, maxWaitTime=10,
            maxIdleTime=180)
        
        fixDraft(sddraft, fixedsddraft, overwrite, jobdir, outputdir)

        # Stage and upload the service if the sddraft analysis did not
        # contain errors
        if analyzeMessages['errors'] == {}:
            # Execute StageService
            arcpy.StageService_server(fixedsddraft, sd)
        else:
            # If the sddraft analysis contained errors, display them
            message = analyzeMessages['errors']
            print (message)
            arcpy.AddMessage(message)
            sys.exit(-1)
    if publish:
        # Execute UploadServiceDefinition
        # Use URL to a federated server
        arcpy.UploadServiceDefinition_server(sd, serverURL)
        message = "Finished publishing {}".format(serviceName)
        print (message)
        arcpy.AddMessage(message)

def fixDraft(sddraft, fixedsddraft, fixoverwrite=False, jobdir=None, outputdir=None):
        doc = DOM.parse(sddraft)
        arcpy.AddMessage("Updating draft: " + sddraft)
        byReference = doc.getElementsByTagName('ByReference')
        for b in byReference:
            if b.firstChild is not None:
                b.firstChild.data = 'true'
        if fixoverwrite:
            rType = doc.getElementsByTagName('Type')
            for t in rType:
                if t.firstChild is not None and t.firstChild.data == 'esriServiceDefinitionType_New':
                    t.firstChild.data = 'esriServiceDefinitionType_Replacement'
                    arcpy.AddMessage("Updating Overwrite in draft")
        PropertySetProperties = doc.getElementsByTagName('PropertySetProperty')
        for t in PropertySetProperties:
            keys = t.getElementsByTagName('Key')
            for key in keys: 
                if outputdir is not None and  key.firstChild is not None and key.firstChild.data == 'outputDir':
                    values = t.getElementsByTagName('Value')
                    for value in values:
                        if hasattr(value.firstChild, 'data'):
                            value.firstChild.data = outputdir
                        else:
                            text = doc.createTextNode(outputdir)
                            value.appendChild(text)
                        arcpy.AddMessage("Set output dir{}".format(outputdir))
                if jobdir is not None and key.firstChild is not None and key.firstChild.data == 'jobsDirectory':
                    values = t.getElementsByTagName('Value')
                    for value in values:
                        if hasattr(value.firstChild, 'data'):
                            value.firstChild.data = jobdir
                        else:
                            text = doc.createTextNode(jobdir)
                            value.appendChild(text)
                        arcpy.AddMessage("Set jobs dir {}".format(jobdir))
        with open(fixedsddraft, 'w', encoding="utf-8") as f:
                doc.writexml( f )

def stageStandalone(result, serviceName,servicefolder,  workdir, executionType, copydata, connection_file_path, stage, publish, overwrite, summary, tags, jobdir, outputdir):
    draftsdir = os.path.join(workdir,"drafts")

    sddraft = os.path.join( draftsdir, serviceName + ".sddraft")
    fixedsddraft = os.path.join( draftsdir,serviceName + "fixed.sddraft")
    sd =os.path.join(workdir, serviceName+ ".sd")

    if stage:
        prepdir(workdir, draftsdir ,sddraft ,sd)

        server_type = "FROM_CONNECTION_FILE"

        # Create service definition draft and return analyzer messages
        analyzeMessages = arcpy.CreateGPSDDraft(
            result, sddraft, serviceName, server_type=server_type,connection_file_path = connection_file_path,
            copy_data_to_server=copydata, folder_name=servicefolder,
            summary=summary , tags=tags, executionType=executionType,
            resultMapServer=False, showMessages="INFO", maximumRecords=5000,
            minInstances=1, maxInstances=1, maxUsageTime=100, maxWaitTime=10,
            maxIdleTime=180)
        
        fixDraft(sddraft, fixedsddraft, overwrite, jobdir, outputdir)

        # Stage and upload the service if the sddraft analysis did not
        # contain errors
        if analyzeMessages['errors'] == {}:
            # Execute StageService
            arcpy.StageService_server(fixedsddraft, sd)
        else:
            # If the sddraft analysis contained errors, display them
            message = analyzeMessages['errors']
            print (message)
            arcpy.AddMessage(message)
            sys.exit(-1)
    if publish:
        # Execute UploadServiceDefinition
        # Use connection file to connect to server
        arcpy.UploadServiceDefinition_server(sd, connection_file_path)
        message = "Finished publishing {}".format(serviceName)
        print (message)
        arcpy.AddMessage(message)

def runAndShare(portal,username, password, server, servicename,servicefolder, toolbox, executionType, copydata, connection_file_path, stage, publish, overwrite, summary, tags, jobdir, outputdir):
    result = runTheTool(toolbox)
    workdir = os.path.join(os.path.dirname(toolbox), "PUB")

    if portal !=''  and username != '' and password != '':
        stageFederated(portal,username, password, result,server, servicename,servicefolder,  workdir, executionType, copydata, connection_file_path, stage, publish, overwrite, summary, tags, jobdir, outputdir)
    else:
        stageStandalone(result, servicename,servicefolder, workdir, executionType, copydata, connection_file_path, stage, publish, overwrite, summary, tags, jobdir, outputdir)

def main(argv):
    opts, args = getopt.getopt(argv,"xe:s:u:p:t:n:f:a:c:o:g:p:r:",["portal=","server=","user=","password=","toolbox=","servicename=", "servicefolder=","executionType=","copydata=", "connectionfile=", "stage=", "publish=", "replace="])
    portal = ''
    server = ''
    username = ''
    password = ''
    toolbox = ''
    servicename = 'GP'
    servicefolder = None
    executionType = 'Synchronous'
    copydata = False
    connection_file_path = ''
    stage = True
    publish = True
    overwrite = False
    jobdir = None 
    outputdir = None


    for opt, arg in opts:
        if opt == '-x':
            print("usage")
            sys.exit()
        elif opt in ("-e", "--portal"):
            portal = arg
        elif opt in ("-s", "--server"):
            server = arg
        elif opt in ("-u", "--user"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-t", "--toolbox"):
            toolbox = arg
        elif opt in ("-n", "--servicename"):
            servicename = arg
        elif opt in ("-f", "--servicefolder"):
            servicefolder = arg
        elif opt in ("-a", "--executionType"):
            executionType = arg
        elif opt in ("-c", "--copydata"):
            copydata = arg == "true"
        elif opt in ("-o", "--connectionfile"):
            connection_file_path = arg
        elif opt in ("-g", "--stage"):
            stage = arg == "true"
        elif opt in ("-p", "--publish"):
            publish = arg == "true"
        elif opt in ("-r", "--overwrite"):
            overwrite = arg == "true"

    runAndShare(portal,username, password, server, servicename,servicefolder, toolbox, executionType, copydata, connection_file_path, stage, publish, overwrite,"Summary", "gp", jobdir, outputdir)





if __name__ == '__main__':
    main(sys.argv[1:])
