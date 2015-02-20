import ogr
import os
import tempfile
import datetime

from opsmanager.ops import BaseOp
from opsmanager.serializers import FileField
from rest_framework import serializers
from rest_framework.exceptions import APIException

def make_buffer(infile,outfile,buffdist):
    
    ds=ogr.Open(infile)
    drv=ds.GetDriver()
    lyr=ds.GetLayer(0)
    
    features = []
    geomcol =  ogr.Geometry(ogr.wkbGeometryCollection)
    for i in range(0,lyr.GetFeatureCount()):
        feat=lyr.GetFeature(i)
        geom=feat.GetGeometryRef()
        feat.SetGeometry(geom.Buffer(float(buffdist)))
        geomcol.AddGeometry(feat.GetGeometryRef())

    out = geomcol.ExportToJson()
    with open(outfile, "wb") as f:
        f.write(out)
    


class BufferParamsSerializer(serializers.Serializer):
    in_file = FileField(help_text='Input file')
    distance = serializers.CharField(help_text='Buffer distance')

    

class BufferOp(BaseOp):

    op_name  = "buffer"
    op_package = "geo"
    op_description = "Create buffers from geometries"
    parameters_serializer = BufferParamsSerializer
    

    def get_dest_extension(self, parameters_dict):
        return ".json"

    def process(self,  parameters):
        
        in_file = parameters.validated_data.pop("in_file")

        #get it on the tmp
        tmp_src = tempfile.NamedTemporaryFile(suffix=in_file.name, delete=False)
        tmp_src.write(in_file.read())
        tmp_src.close()
        
        #get a tmp filename for dst
        tmp_dst=  tmp_src.name + self.get_dest_extension(parameters.validated_data)
        
        try:
          msg = make_buffer(tmp_src.name, tmp_dst, parameters.validated_data['distance'])

        except Exception, e:
          print e
          raise APIException(detail=str(e))

        return { "filename" : tmp_dst }

