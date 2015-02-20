from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
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
        meta = { 'name' : self.op_name, 'description' : self.op_description , 'package':self.op_package}
        meta['parameters'] = self.get_parameters_meta()
        meta['abs_url'] = request.build_absolute_uri(self.op_name + "/")
        meta['url'] = BASE_OPS_URL + '/' + self.op_name 

        return meta

    
    def get(self, request, format=None):
        return Response(self.get_meta(request))


    def post(self, request, format=None):
        if getattr(self,"parameters_serializer" , None):
            parameters = self.parameters_serializer(data=request.data)
            parameters.is_valid(raise_exception=True)
        else:
            parameters = {}

        
        try:
            out_file = self.process(parameters)
            print out_file
            out_response = export_file(out_file['filename'])
        except Exception, e:
            raise e
        
        return Response(out_response)




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

"""

OP PROPERTIES
name : important for urls
file inputs : should describe accepted file types for each of the file inputs. we require correct mimetype
params : parameters that will be passed to the process function.
    we could give hints for validation, allowing client side validation



OP PROCESS    

- gets file(s) from data and stores them in temp filesystem
- runs process method on files in temp filesystem, with params and returns processed files(s), embedded as json
  (in case of error just raise it) 


"""