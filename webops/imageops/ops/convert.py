import tempfile
import subprocess
import datetime
from opsmanager.ops import BaseOp
from opsmanager.helpers import write_to_temp
import os

from rest_framework import serializers
from rest_framework.exceptions import APIException


class ConvertParamsSerializer(serializers.Serializer):
    in_file = serializers.FileField(help_text='Input file')
    #should be choiceField!
    f = serializers.CharField(help_text='Target extension')
    


class ConvertOp(BaseOp):

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
    
        in_file = parameters.validated_data["in_file"]

        #get it on the tmp
        tmp_src = write_to_temp(in_file)
        
        #get a tmp filename for dst
        tmp_dst=  tmp_src + self.get_dest_extension(parameters.validated_data)

        #appending args [files]
        cmd.append(tmp_src)
        cmd.append(tmp_dst)
        
        
        try:
          msg = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        except Exception, e:
          print e.output
          raise APIException(detail=str(e.output))

        return { "filename" : tmp_dst }

    
