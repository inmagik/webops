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


def write_to_temp(in_file):
    #get it on the tmp
    tmp_src = tempfile.NamedTemporaryFile(suffix=in_file.name, delete=False)
    tmp_src.write(in_file.read())
    tmp_src.close()
    return tmp_src.name
        




def make_serializer(name, **kwattrs):
    return type(name, (serializers.Serializer,), dict(**kwattrs))



from rest_framework import serializers
def serializer_from_dict(nm, data):

    fields = {}
    for k in data.keys():
        item = data[k]
        kls = item["serializer_class"]
        params = item["kwargs"]

        field_klass = getattr(serializers, kls)
        fields[k] = field_klass(**params)

    return make_serializer(nm, **fields)




