#WEBOPS -- example site

Cloud based service that provides access to running remote "operations" on the cloud.

It provides:
* REST api to get metadata about accessible operations and endpoints to run them (based ond Django)
* a web interface to configure and run operations (based on Angular)
* a command line interface to access API from the bash (not here yet)
* libs for accessing the API from different languages via HTTP (Not here yet). First candidates are javascript and python, to be used in the web and command line interfaces.

Currently the project is focused on operations that output files, in particular operations on geographical data and images.
Some operations will be included in the project itself, but on the long term this will be a container/framework and operations will be added by other django apps. 

## SETUP 
Activate your environment, then update requirments
    
    pip install -r requirements.txt


## UP AND RUNNING:
Start django server

    cd webops
    python manage.py runserver


During developement point browser to:

    http://localhost:8000/static/www/index.html





# REST API



## OPS LIST
	
	GET /ops/
	
	HTTP 200 OK
    Content-Type: application/json
    Vary: Accept
    Allow: GET, HEAD, OPTIONS

    [
        {
            "abs_url": "http://localhost:8000/ops/ogr2ogr/", 
            "parameters": {
                "t_srs": {
                    "required": false, 
                    "type": "CharField", 
                    "description": "Reproject/transform to this SRS on output", 
                    "choices": null
                }, 
                "a_srs": {
                    "required": false, 
                    "type": "CharField", 
                    "description": "Assign an input SRS", 
                    "choices": null
                }, 
                "in_file": {
                    "required": true, 
                    "type": "FileField", 
                    "description": "Input file", 
                    "choices": null
                }, 
                "f": {
                    "required": true, 
                    "type": "ChoiceField", 
                    "description": "Format name", 
                    "choices": {
                        "GeoJSON": "GeoJSON", 
                        "CSV": "CSV", 
                        "GML": "GML", 
                        "GPX": "GPX", 
                        "KML": "KML", 
                        "SQLite": "SQLite", 
                        "GMT": "GMT", 
                        "GPKG": "GPKG", 
                        "DXF": "DXF", 
                        "Geoconcept": "Geoconcept", 
                        "GeoRSS": "GeoRSS", 
                        "PGDump": "PGDump", 
                        "ODS": "ODS", 
                        "XLSX": "XLSX", 
                        "ESRI Shapefile": "ESRI Shapefile", 
                        "MapInfo File": "MapInfo File"
                    }
                }
            }, 
            "package": "geo", 
            "url": "ops/ogr2ogr", 
            "description": "Use ogr2ogr to convert geographical vector file formats", 
            "name": "ogr2ogr"
        },
        {
            "abs_url": "http://localhost:8000/ops/pdftotext/", 
            "parameters": {
                "in_file": {
                    "required": true, 
                    "type": "FileField", 
                    "description": "Input file", 
                    "choices": null
                }
            }, 
            "package": "image", 
            "url": "ops/pdftotext", 
            "description": "Extract text from pdf files", 
            "name": "pdftotext"
        }
    ]



## OP META

	GET /webops/<op-name>/


## RUNNING AN OP
	
	POST /webops/<op-name>/
	
When POST is issued against an op, the server returns a json object containing the output file as base64 encoded data.

    {
        data : "...",
        filename : "a.jpg",
        path : ".." 
    }

    data: contains the base64 encoded file
    filename: filename proposed
    path: the original path on server (will be changed soon to something more useful)


# Django API

    
## ADDING OPS

New operations can be added by creating a `webops.py` file in your application.
This file is responsibile for registering new operations.

API will be documented soon ... for now look at the included `geoops` and `imageops` apps included in the project.



### Creating an op

Creating an op is done by subclassing the `BaseOp` class. Here is a piece of the declaration of the OgrOp

    
    class OgrOp(BaseOp):

        op_name  = "ogr2ogr"
        op_package = "geo"
        op_description = "Use ogr2ogr to convert geographical vector file formats"
        parameters_serializer = OgrParamsSerializer
        ...



### INPUT DESCRIPTORS
### PROCESS FUNCTION
### CHECK FUNCTION



### Registering an op


# SETTINGS

WEBOPS_BREAK_ON_FAIL_TEST: if set to true, webserver won't start if any registration test fails







