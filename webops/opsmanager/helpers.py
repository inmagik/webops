import tempfile
import json

import os
import zipfile
import base64

def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file), file)
    


def export_file(path):

    with open(path) as f:
        data = base64.b64encode(f.read())

    filename = os.path.basename(path)
    
    return { 
                'data' : data, 
                'path' : path,
                'filename' : filename
            }

