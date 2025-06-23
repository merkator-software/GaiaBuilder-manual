Publish a Geoprocessing service
=======================
> **Note:** Throughout this document, the term **GeoProcessing** will be abbreviated as **GP**.

### 🧠 Assumptions

You are an ArcGIS Pro user who knows how to:

* Publish a GP service and know how to create a python toolbox, as well as how to test run a GP service in python
* Configure thumbnails, metadata, terms of use, and group sharing
* High level knowledge of GaiaBuilder to manage deployments through JSON
* Use version control systems like Git, Subversion or Bitbucket

---
### Overview

```mermaid
graph LR
  gaiabuilder[Copy the Template folder for GeoProcessingService]
  configure[Ammend stage.py for each GP to run once.]
  gp[Create python toolbox and the GP tool]
  git[Git Repository]
  pipeline[CI/CD Pipeline]
  portal[Published GP service on Enterpise Portal prod]
  edit[Create gpservice.json]
  server[Create server.json]

  gp --> gaiabuilder
  gaiabuilder --> configure
  configure --> git
  gp --> git
  edit --> git
  server --> git
  git --> pipeline
  pipeline --> portal
```

### ✅ Step-by-Step Deployment Flow

1. **Create your GP in ArcGIS Pro**
   Create your GP service in ArcGIS Pro, including the necessary Python toolbox and GP tool and metadata xml files. Ensure that the GP tool is tested and runs successfully in ArcGIS Pro.

2. **Create `gpservice.json`**
    
   From the example template, create a `gpservice.json` file that defines the GP service configuration. This file will be used by GaiaBuilder to deploy the GP service, as it needs to be run at least once.

   The `gpservice.json` file references the GP service pyt file using the `toolbox` parameter, which will be used during the publishing process to create the GP service.
   This file including the metadata XML files should be relative to the gpservice.json file.

<Details><Summary>Expand for example gpservice.json</Summary>

The `gpservice.json` file contains various properties that define the GP service, such as its name, description, categories, tags, and server configuration. The `toolbox` property points to the toolbox pyt file, it should be accompanied with the toolbox and tool metadata XML.
For an overview what each attribute does, see the [GP JSON configuration](https://github.com/merkator-software/GaiaBuilder-manual/wiki/GP-JSON-configuration).

```json
{
  "action": "publishSD",
  "stageScript": "stage.py",
  "toolbox": "Demo_GP_Service.pyt",
  "content_status": "authoritative",
  "protected": "true",
  "credits": "Copyright Contoso",
  "description": "Contoso Python Geoprocessing service example.",
  "extensions": [
  ],
  "executionType": "Asynchronous",
  "copyData": "true",
  "maxIdleTime": 1800,
  "maxInstancesPerNode": 3,
  "maxStartupTime": 300,
  "maxUsageTime": 600,
  "maxWaitTime": 60,
  "minInstancesPerNode": 1,
  "name": "Add_Number_Service_DEV",
  "portalFolder": "dev",
  "portalLogo": "gp_thumbnail_dev.png",
  "recycleInterval": 24,
  "recycleStartTime": "00:00",
  "serverFolder": "DEV",
  "categories": [
    "/Categories/Democategory",
    "/Categories/Administrative data"
  ],
  "serverconfiguration": "server.json",
  "serviceType": "GPServer",
  "summary": "Contoso GP service summary example.",
  "tags": "Geoprocessing,Service,Contoso,Example,Basic math,Add",
  "uselimitations": "For demonstration purposes only."
}

```
</Details>

3. **Create `service.json`**

The `service.json` file defines the server configuration for the print service, including the server folder, portal folder, data sources, and sharing settings.
   
<Details><Summary>Expand for example service.json</Summary>

The properties in the `service.json` file are used to configure the print service for different environments (e.g., DEV, TEST, ACC, PROD). Each environment has its own server folder, portal folder, data sources, and sharing settings.

```json
{
  "servers": {
    "ACC": {
      "serverFolder": "ACC",
      "portalFolder": "acc",
      "datasources": [
      ],
      "sharing": {
        "groups": [
          "Demo ACC"
        ],
        "organization": "false",
        "public": "false"
      },
      "name": "Add_Number_Service_ACC",
      "portalLogo": "gp_thumbnail_acc.png"
    },
    "PROD": {
      "serverFolder": "PROD",
      "portalFolder": "prod",
      "datasources": [
      ],
      "sharing": {
        "groups": [
          "Demo PROD"
        ],
        "organization": "false",
        "public": "false"
      },
      "name": "Add_Number_Service_PROD",
      "portalLogo": "gp_thumbnail_prod.png"
    },
    "TEST": {
      "serverFolder": "TEST",
      "portalFolder": "test",
      "datasources": [
      ],
      "sharing": {
        "groups": [
          "Demo TEST"
        ],
        "organization": "false",
        "public": "false"
      },
      "name": "Add_Number_Service_TEST",
      "portalLogo": "gp_thumbnail_test.png"
    },
    "DEV": {
      "serverFolder": "DEV",
      "portalFolder": "dev",
      "datasources": [
      ],
      "sharing": {
        "groups": [
          "Demo DEV"
        ],
        "organization": "false",
        "public": "false"
      },
      "name": "Add_Number_Service_DEV",
      "portalLogo": "gp_thumbnail_dev.png"
    }
  }
}
```
</Details>


3. **Commit and push to version control**

   Store the JSON files, and layouts in the template folder in Git (or other VCS) for reproducible deployments and rollback support.

<Details><Summary>List of the files stored in git on our environment</Summary>                                                                                                                                                                                                                                                                                                                      

    ## 📁 Project Files Overview

    - 🧮 `Demo_GP_Service.AddNumbers.pyt.xml`
    - 🧰 `Demo_GP_Service.pyt`
    - 📝 `Demo_GP_Service.pyt.xml`
    - 🗂️ `gpservice.json`
    - 🖼️ `gp_thumbnail_acc.png`
    - 🖼️ `gp_thumbnail_dev.png`
    - 🖼️ `gp_thumbnail_prod.png`
    - 🖼️ `gp_thumbnail_test.png`
    - 🗄️ `server.json`
    - 🐍 `stage.py`
    - 🏁 `__init__.py`
</Details>

## 🧪 Generic Deployment Script (PowerShell)

This example works on any runner or agent that supports PowerShell and Python (with Conda) [^1]. It uses the gpservice.json created ($env:manual_build_list) above, including the relative path and the environment name ($env:server) where you want to push it to 1.

```powershell
 # Activate the required Conda environment
& "$env:CondaHook"
conda activate "$env:CondaEnv_GaiaBuilder"

# Define the path to the content installer script
$scriptPath = "C:\GaiaBuilder\InstallGeoProcessor_lite.py"

# Required arguments:
# -f: Path to the build list JSON file
# -s: Target server config name
$args = @(
    "-f", $env:manual_build_list,
    "-s", "${{ parameters.server }}"
)

# Execute the GaiaBuilder Geo Processor installer script
Write-Host "Executing GaiaBuilder content install with args: $args"
python $scriptPath $args
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: GP service installer failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
} else {
    Write-Host "✅ GP service installed successfully"
}
```

### 🔐 Environment Variables

The -u and -p arguments are not safe to use in most CI environments and are intended for standalone use only.
Instead, set these values securely using your CI/CD environment's secret store:

```yaml
env:
  USER: $(USER)
  PASSWORD: $(PASSWORD)
```

This ensures your credentials do not appear in logs or version control.

---
After deployment, verify your map service in the ArcGIS REST Services Directory or ArcGIS Pro Catalog before promoting to higher environments.


[^1]: ## 🧾 GaiaBuilder CLI Options
InstallGeoProcessorTool and the light version (without an arcpy dependency) command line options are documented [here](https://github.com/merkator-software/GaiaBuilder-manual/wiki/InstallGeoProcessorTool)


