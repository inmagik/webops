#WEBOPS
## WHAT'S THIS?
It's cloud based service that provides access to running remote "operations" on the cloud.
It provides:
* REST api to get metadata about accessible operations and endpoints to run them (based ond Django)
* a web interface to configure and run operations (based on Angular)
* a command line interface to access API from the bash (not here yet)
* possibly various wrappers for accessing the API from different languages. (not here yet, first candidata is python)

Currently the project is focused on operations that output files, in particular operations on geographical data and images.
In the early stages of the project, some operations will be included in the project itself, but on the long term this will be a container/framework and operations will be added by other django apps. 

## SETUP 
Activate your environment, then update requirments
    
    pip install -r requirements.txt


## UP AND RUNNING:
Start django server

    cd webops
    python manage.py runserver


During developement point browser to:

    http://localhost:8000/static/www/index.html


    
## ADDING OPS
New operations can be added by creating a `webops.py` file in your application.
This file is responsibile for registering new operations.

API will be documented soon ... for now look at the included `geoops` and `imageops` apps included in the project.
