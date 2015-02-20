import tempfile
import subprocess
import datetime
import os

from opsmanager.ops import BaseOp
from rest_framework import serializers
from rest_framework.exceptions import APIException

OGR_SUPPORTED_FORMATS = ["GeoJSON", "CSV", "GML", "GPX" ,"KML", "SQLite", "GMT", "GPKG", 
    "DXF", "Geoconcept", "GeoRSS", "PGDump", "ODS", "XLSX", ""]


class OgrParamsSerializer(serializers.Serializer):
    in_file = serializers.FileField(help_text='Input file')
    #should be choiceField!
    a_srs = serializers.CharField(help_text='Assign an input SRS',required=False)
    t_srs = serializers.CharField(help_text='Reproject/transform to this SRS on output',required=False)
    f = serializers.ChoiceField(help_text='Format name', choices=OGR_SUPPORTED_FORMATS)
    


class OgrOp(BaseOp):

    op_name  = "ogr2ogr"
    op_package = "geo"
    op_description = "Use ogr2ogr to convert geographical vector file formats"
    parameters_serializer = OgrParamsSerializer

    
    @classmethod
    def check_op(self):
        """
        This class method is called before registering operation.
        It's optional.
        """
        cmd = ["ogr2ogr", "--help"]
        devnull = open(os.devnull, 'w')
        subprocess.call(cmd, stdout=devnull, stderr=devnull)

    
    def get_dest_extension(self, parameters_dict):
        """
        """
        return "."+parameters_dict['f']
        
    
    def process(self, parameters):
        
        cmd = ["ogr2ogr"]

        in_file = parameters.validated_data.pop("in_file")
        
        #appending params
        for key in parameters.validated_data:
            cmd.append("-" + key)
            cmd.append('%s' % str(parameters.validated_data[key]))
            
        #get it on the tmp
        tmp_src = tempfile.NamedTemporaryFile(suffix=in_file.name, delete=False)
        tmp_src.write(in_file.read())
        tmp_src.close()
        
        tmp_dst=  tmp_src.name + self.get_dest_extension(parameters.validated_data)

        #appending args [files]
        cmd.append(tmp_dst)
        cmd.append(tmp_src.name)
        
        
        try:
          msg = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        except Exception, e:
            print e.output
            raise APIException(detail=str(e.output))

        return { "filename" : tmp_dst }

