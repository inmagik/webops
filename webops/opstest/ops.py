from opsmanager.ops import BaseOp
from opsmanager.helpers import write_to_temp, unzip_to_temp, zip_to_temp
from opsmanager.serializers import SingleFileParamsSerializer

class DummyOp(BaseOp):

    op_name  = "dummy"
    op_package = "files"
    op_description = "Takes a file and sends it back"
    parameters_serializer = SingleFileParamsSerializer

    
    def process(self,  parameters):
        
        in_file = parameters.pop("in_file")
        tmp_src = write_to_temp(in_file)
        
        return { "filename" : tmp_src }