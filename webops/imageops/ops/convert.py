import tempfile
import subprocess
import datetime
from webops_django.ops import BaseOp
from webops_django.helpers import write_to_temp
from webops_django.serializers import FileField 
import os

from rest_framework import serializers
from rest_framework.exceptions import APIException
from .imagemagik_formats import get_imagemagik_formats

SUPPORTED_IMAGE_FORMATS = get_imagemagik_formats()


class ConvertParamsSerializer(serializers.Serializer):
    in_file = FileField(help_text='Input file')
    #should be choiceField!
    f = serializers.CharField(help_text='Target extension')
    #choices=OGR_SUPPORTED_FORMATS
    #f = serializers.ChoiceField(help_text='Target extension', choices=SUPPORTED_IMAGE_FORMATS)
    


class ConvertOp(BaseOp):
    op_id = "com.inmagik.convert"
    op_name  = "convert"
    op_package = "image"
    op_description = "Use imagemagik convert to convert image file formats"
    parameters_serializer = ConvertParamsSerializer
    

    @classmethod
    def check_op(self):
        """
        This class method is called before registering operation.
        It's optional.
        """
        cmd = ["convert", "--help"]
        devnull = open(os.devnull, 'w')
        subprocess.call(cmd, stdout=devnull, stderr=devnull)

    
    def get_dest_extension(self, parameters_dict):
        """
        """
        return "."+parameters_dict['f']
        
    
    def process(self, parameters):
        
        
        cmd = ["convert"]
    
        in_file = parameters["in_file"]

        #get it on the tmp
        tmp_src = write_to_temp(in_file)
        
        #get a tmp filename for dst
        tmp_dst=  tmp_src + self.get_dest_extension(parameters)

        #appending args [files]
        cmd.append(tmp_src)
        cmd.append(tmp_dst)
        
        
        try:
          msg = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        except Exception, e:
          print e.output
          raise APIException(detail=str(e.output))

        return { "filename" : tmp_dst }

    
