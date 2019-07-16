# powerwatch-site-selection
Treatment and control site selection starter guide

This guide is aimed to set up the requirements for building a low voltage distribution line network and execture the code which generates treatment and control sites

System requirements:
Arcmap is required to run each of the programs
ArcGIS license can be obtained through UC Berkeley
ArcGIS runs exclusively on windows. Running in a Mac requires either a virtual machine or a remote desktop
If running on a personal Mac, setting up a remote desktop through AWS is preferrable as it does not require an external hard drive or partitioning


Steps to install ArcGIS:
Download ArcGIS through the UC Berkeley software portal
Obtain software license through the Berkeley Geospatial Innovaition Facility (GIF). This can be done over email
	GIF is a local resource which can help troubleshoot GIS problems
	Appointments for consultation can be set up through the GIF online portal http://gif.berkeley.edu/support/office_hours.html
Install ArcGIS Suite and enter license
Extensions required for the analysis are the Network Analyst and Spatial Analyst


Loading desired files into ArcMap:
Launch ArcMap and create a blank document
In the launch window, you can select the default geodatabase where all of the intermadiate files are stored. The default is the ArcGIS default geodatabase
In the ArcCatalog window, connect to the root folder where the desired Accra shapefiles are saved. Here you can browse files and add data to the workspace window
Locate the files by either dragging files from the Catalog window into the workspace or using the "Add Data" feature and locating the files

If a network dataset for a district in question exists, loading the network dataset into the workspace (dataframe) will prompt asking to load the associated feature classes (shapefiles). Agree to this
When running the python script for the analysis, variables associated with layers can either be set by locating their path or by referring to loaded layers by their name in single quotes i.e 'Existing_transformers'


Running python scripts:
The python script window allows you to run essential ArcMap functions. Arcpy functions essentially choose ArcGIS tools, set the inputs, outputs, and settings, and then run the function
Open Python window in ArcMap
Alternatively, you can use the python console, but this requires additional setup to integrate with ArcMap which is not covered in this tutorial
In this window you can write or paste any code from the programs provided
Before running the script, you can check each command, and a description of the command and inputs will appear in the console to the right

# To Access Encrypted Data

There is a keybase encrypted data repository that we use internally. It is
placed as a submodule of this repo. To access it you must first be part of the
gridwatch keybase team, then run:

```
$ git config --global --add protocol.keybase.allow always
```

in your terminal to enable git to transport keybase repos as submodules.

If you do both of these things then

```
$ git clone --recursive git@github.com:lab11/powerwatch-site-selection
```
should work as expected. If you already have the repository you can run:

```
$ git submodule update --init --recursive
```

to get the submodule.
