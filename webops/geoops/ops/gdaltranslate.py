import tempfile
import subprocess
import datetime

from opsmanager.ops import BaseOp
from opsmanager.serializers import FileField 


from rest_framework import serializers
from rest_framework.exceptions import APIException
 
from .gdal_formats import GDAL_TRANSLATE_SUPPORTED_FORMATS



class TranslateParamsSerializer(serializers.Serializer):
    of = serializers.ChoiceField(help_text='Format name', choices=GDAL_TRANSLATE_SUPPORTED_FORMATS)
    in_file = FileField(help_text='Input file')
    

class GDALTranslateOp(BaseOp):

    op_name  = "gdal_translate"
    op_package = "geo"
    op_description = "Use gdal_translate to convert geographical raster file formats"
    parameters_serializer = TranslateParamsSerializer
    
    
    def get_dest_extension(self, parameters_dict):
        """
        """
        return "."+parameters_dict['of']
        
    
    def process(self, parameters):
        
        cmd = ["gdal_translate"]
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
        cmd.append(tmp_src.name)
        cmd.append(tmp_dst)
        
        
        try:
          msg = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        except Exception, e:
          print e.output
          raise APIException(detail=str(e.output))

        return { "filename" : tmp_dst }

