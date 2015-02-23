import tempfile
import subprocess
import datetime
import os
import mimetypes
import glob
import shutil

from opsmanager.ops import BaseOp
from opsmanager.helpers import write_to_temp, unzip_to_temp, zip_to_temp
from opsmanager.serializers import FileField 

from rest_framework import serializers
from rest_framework.exceptions import APIException

OGR_SUPPORTED_FORMATS = ["GeoJSON", "CSV", "GML", "GPX" ,"KML", "SQLite", "GMT", "GPKG", 
    "DXF", "Geoconcept", "GeoRSS", "PGDump", "ODS", "XLSX", "ESRI Shapefile", "MapInfo File"]


class OgrParamsSerializer(serializers.Serializer):
    in_file = FileField(help_text='Input file')
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
        if(parameters_dict['f'] == 'ESRI Shapefile'):
            return ".shp"
        if(parameters_dict['f'] == 'MapInfo File'):
            return ".tab"

        return "."+parameters_dict['f']
    

    def get_main_src(self, filelist):
        
        for x in filelist:
            xx = x.lower()
            if xx.endswith("shp") or xx.endswith("tab"):
                return x
        return filelist[0]

    def pack_output(self, tmp_dst, parameters):
        if tmp_dst.endswith(".shp") or tmp_dst.endswith(".tab"):
            base_path = os.path.dirname(tmp_dst)
            base_name, ext = os.path.splitext(tmp_dst)
            files = glob.glob(os.path.join(base_path, base_name+"*"))
            files = [x for x in files if not x.endswith(base_name)]
            out = zip_to_temp(files)
            return out
        else:
            return tmp_dst

    
    def process(self, parameters):
        
        cmd = ["ogr2ogr"]

        in_file = parameters.pop("in_file")
        
        #appending params
        for key in parameters:
            cmd.append("-" + key)
            cmd.append('%s' % str(parameters[key]))
            
        #get it on the tmp
        #get it on the tmp
        mime = mimetypes.guess_type(in_file.name)
        zipfile = mime[0] == 'application/zip'
        
        if not zipfile:
            tmp_src = write_to_temp(in_file)
        else:
            tmp_srcs = unzip_to_temp(in_file)
            tmp_src = self.get_main_src(tmp_srcs)


        tmp_dst= tmp_src + self.get_dest_extension(parameters)

        #appending args [files]
        cmd.append(tmp_dst)
        cmd.append(tmp_src)
        
        
        try:
          msg = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        except Exception, e:
            print e.output
            raise APIException(detail=str(e.output))
        
        #zip up files if needed
        out_file = self.pack_output(tmp_dst,parameters)

        return { "filename" : out_file }

