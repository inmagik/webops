from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .register import _register

class OpsView(APIView):
    """
    
    """
    op_description = ""
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        """
        Return a list of all ops.
        """
        ops = _register.ops
        out = []
        for op in ops:
            out.append(ops[op].get_meta(request))
        return Response(out)


    

