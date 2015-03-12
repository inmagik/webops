from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.exceptions import APIException
from .helpers import export_file

BASE_OPS_URL = 'ops'

class BaseOp(APIView):

    #permission_classes = (permissions.AllowAny,)
    op_package = "webops"

    @classmethod
    def check_op(self):
        raise NotImplementedError
    
    @classmethod
    def get_parameters_meta(self):
        out = {}
        if not getattr(self,"parameters_serializer" , None):
            return out
        fields = self.parameters_serializer().get_fields()
        for field in fields:
            out[field] = { 
                'type' : fields[field].__class__.__name__ ,
                'description' : fields[field].help_text,
                'choices' : getattr(fields[field], 'choices', None),
                'required' : getattr(fields[field], 'required', None),
                }

        return out

    
    @classmethod
    def get_meta(self, request):
        meta = { 'id' : self.op_id, 'name' : self.op_name, 'description' : self.op_description , 'package':self.op_package}
        meta['parameters'] = self.get_parameters_meta()
        meta['abs_url'] = request.build_absolute_uri(self.op_id + "/")
        meta['url'] = BASE_OPS_URL + '/' + self.op_id 
        output_descriptor = getattr(self, 'output_descriptor', None)
        if output_descriptor:
            meta['output_descriptor'] = self.output_descriptor.__class__.__name__
        else:
            meta['output_descriptor'] = 'FileData'

        return meta

    
    def get(self, request, format=None):
        return Response(self.get_meta(request))


    def post(self, request, format=None):
        if getattr(self,"parameters_serializer" , None):
            parameters = self.parameters_serializer(data=request.data)
            parameters.is_valid(raise_exception=True)
        else:
            parameters = {}

        
        if not self.output_descriptor:
            try:
                out_file = self.process(parameters.validated_data)
                #print out_file
                out_response = export_file(out_file['filename'])
            except Exception, e:
                #print str(e)
                #raise e

                raise APIException(detail=str(e))
        else:
            try:
                out_data = self.process(parameters.validated_data)
                #print out_file
                out_response = self.output_descriptor.to_representation(out_data)
            except Exception, e:
                raise APIException(detail=str(e))
            
        
        return Response(out_response)

