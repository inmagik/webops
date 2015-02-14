import tempfile
import subprocess
import datetime
from opsmanager.register import _register
from opsmanager.ops import BaseOp

from rest_framework import serializers
from rest_framework.exceptions import APIException

from buffer_ops import make_buffer
        







class ConvertParamsSerializer(serializers.Serializer):
    #should be choiceField!
    f = serializers.CharField(help_text='Target extension')
    

class ConvertFilesSerializer(serializers.Serializer):
    in_file = serializers.FileField(help_text='Input file')


class ConvertOp(BaseOp):

    op_name  = "convert"
    op_description = "Use imagemagik convert to convert image file formats"
    parameters_serializer = ConvertParamsSerializer
    files_serializer = ConvertFilesSerializer
    
    def get_dest_extension(self, parameters_dict):
        """
        """
        return "."+parameters_dict['f']
        
    
    def process(self, files, parameters):
        
        
        cmd = ["convert"]
    
        in_file = files.validated_data["in_file"]

        #get it on the tmp
        tmp_src = tempfile.NamedTemporaryFile(suffix=in_file.name, delete=False)
        tmp_src.write(in_file.read())
        tmp_src.close()
        
        #get a tmp filename for dst
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

    



"""
ops list:
* ops names, descriptions, urls

each op should have:
* input file(s) description. each op take at least (and only for now) a file as input.
  these are ops on file that return files.
* params description: note that there are a lot of options:
  - params combinations: the user should not be able to use params combo known to be
    wrong a priori.
  - params depending on other params
  - params depending on input file(s) contents. 

* post view/url to execute op
  this url returns a file that will be cached (in the webpage, as a blob) 
  and served by the browser (via javascript, with link on page - content is in the browser)
  the url will be built using op name.

* a process function, called by the view.
  this will be overridden in each op class






"""