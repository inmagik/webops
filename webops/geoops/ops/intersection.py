import ogr
import os
import tempfile
import datetime

from opsmanager.ops import BaseOp
from opsmanager.serializers import FileField 

from rest_framework import serializers
from rest_framework.exceptions import APIException


def make_intersection(InFile1,InFile2,outfile):

    with open(InFile1) as f1, open(InFile2) as f2:
        data1 = f1.read()
        data2 = f2.read()

        a = ogr.CreateGeometryFromJson(data1)
        b = ogr.CreateGeometryFromJson(data2)
        out = a.Intersection(b)
        geomcol =  ogr.Geometry(ogr.wkbGeometryCollection)
        geomcol.AddGeometry(out)
        json = geomcol.ExportToJson()

        with open(outfile, "wb") as f:
            f.write(json)





class IntersectionParametersSerializer(serializers.Serializer):

    in_file1 = FileField(help_text='Input file')
    in_file2 = FileField(help_text='Input file')



class IntersectionOp(BaseOp):
    op_id = "com.inmagik.geojsonintersection"
    op_name  = "Intersection"
    op_package = "geo"
    op_description = "Create intersection from two geojson"
    parameters_serializer = IntersectionParametersSerializer




    def process(self, parameters):

        file1 = parameters["in_file1"]
        file2 = parameters["in_file2"]

        #get it on the tmp
        tmp_src1 = tempfile.NamedTemporaryFile(suffix=file1.name, delete=False)
        tmp_src1.write(file1.read())
        tmp_src1.close()

        tmp_src2 = tempfile.NamedTemporaryFile(suffix=file1.name, delete=False)
        tmp_src2.write(file2.read())
        tmp_src2.close()

        #get a tmp filename for dst
        tmp_dst=  tmp_src1.name + ".geojson"


        try:
          msg = make_intersection(tmp_src1.name, tmp_src2.name, tmp_dst)

        except Exception, e:
          print e
          raise APIException(detail=str(e))

        return { "filename" : tmp_dst }
