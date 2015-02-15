import tempfile
import subprocess
import datetime
from opsmanager.ops import BaseOp

from rest_framework import serializers
from rest_framework.exceptions import APIException

 

class ConvertFilesSerializer(serializers.Serializer):
    in_file = serializers.FileField(help_text='Input file')


class PDFToTextOp(BaseOp):

    op_name  = "pdftotext"
    op_package = "image"
    op_description = "Extract text from pdf files"
    files_serializer = ConvertFilesSerializer
    
        
    
    def process(self, files, parameters):
        
        
        cmd = ["pdftotext"]
    
        in_file = files.validated_data["in_file"]

        #get it on the tmp
        tmp_src = tempfile.NamedTemporaryFile(suffix=in_file.name, delete=False)
        tmp_src.write(in_file.read())
        tmp_src.close()
        
        #get a tmp filename for dst
        tmp_dst=  tmp_src.name.replace(".pdf", ".txt")

        #appending args [files]
        cmd.append(tmp_src.name)
        
        
        try:
          msg = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        except Exception, e:
          print e.output
          raise APIException(detail=str(e.output))

        return { "filename" : tmp_dst }

    
