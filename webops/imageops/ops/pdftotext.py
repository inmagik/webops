import tempfile
import subprocess
import datetime
from webops_django.ops import BaseOp
from webops_django.helpers import write_to_temp
from rest_framework import serializers
from rest_framework.exceptions import APIException

from webops_django.serializers import FileField 

class ConvertParametersSerializer(serializers.Serializer):
    in_file = FileField(help_text='Input file')


class PDFToTextOp(BaseOp):
    op_id = "com.inmagik.pdftotext"
    op_name  = "pdftotext"
    op_package = "image"
    op_description = "Extract text from pdf files"
    parameters_serializer = ConvertParametersSerializer
    
        
    
    def process(self, parameters):
        
        
        cmd = ["pdftotext"]
    
        in_file = parameters["in_file"]

        #get it on the tmp
        tmp_src = write_to_temp(in_file)
        
        #get a tmp filename for dst
        tmp_dst=  tmp_src.replace(".pdf", ".txt")

        #appending args [files]
        cmd.append(tmp_src)
        
        
        try:
          msg = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        except Exception, e:
          print e.output
          raise APIException(detail=str(e.output))

        return { "filename" : tmp_dst }

    
