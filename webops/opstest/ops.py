from opsmanager.ops import BaseOp
from opsmanager.helpers import write_to_temp, unzip_to_temp, zip_to_temp
from opsmanager.serializers import SingleFileParamsSerializer
from rest_framework import serializers

class DummyOp(BaseOp):

    op_id = "com.inmagik.opstest-dummyop"
    op_name  = "dummy"
    op_package = "files"
    op_description = "Takes a file and sends it back"
    parameters_serializer = SingleFileParamsSerializer

    
    def process(self,  parameters):
        
        in_file = parameters.pop("in_file")
        tmp_src = write_to_temp(in_file)
        
        return { "filename" : tmp_src }



class SupOpInputSerializer(serializers.Serializer):
    a = serializers.FloatField()
    b = serializers.FloatField()


class SumOp(BaseOp):

    op_id = "com.inmagik.opstest-sum"
    op_name  = "sum numbers"
    op_package = "numbers"
    op_description = "Sums to numbers"
    parameters_serializer = SupOpInputSerializer
    output_descriptor = serializers.FloatField()

    
    def process(self,  parameters):
        return parameters['a'] + parameters['b']