import os
import tempfile
import datetime

from webops_django.ops import BaseOp
from webops_django.serializers import FileField
from webops_django.helpers import write_to_temp

from rest_framework import serializers
from rest_framework.exceptions import APIException

import geopy

def geocode(line):
    from geopy.geocoders import GoogleV3
    geolocator = GoogleV3()
    try:
        location = geolocator.geocode(line)
        return location
    except:
        return None

    



class GeocodeParamsSerializer(serializers.Serializer):
    in_file = FileField(help_text='Input file')
    

class GeocodeOp(BaseOp):
    op_id = "com.inmagik.geocode"
    op_name  = "geocode"
    op_package = "geo"
    op_description = "Takes a text file with addresses and returns a csv with geolocated addresses"
    parameters_serializer = GeocodeParamsSerializer
    

    
    def process(self,  parameters):
        
        in_file = parameters.pop("in_file")

        #get a tmp filename for dst
        tmp_dst_file = tempfile.NamedTemporaryFile(suffix=in_file.name, delete=False)
        for d in in_file.readlines():
            line = d.replace("\r", "").replace("\n", "")
            geo = geocode(line)
            if geo:
                codedline = '"%s", "%s", %s, %s' % (line, geo.address, geo.latitude, geo.longitude) 
            else:
                codedline = d
            tmp_dst_file.write(codedline+"\r\n")


        tmp_dst_file.close()
        tmp_dst = tmp_dst_file.name
        
        try:
            pass

        except Exception, e:
          raise APIException(detail=str(e))

        return { "filename" : tmp_dst }

