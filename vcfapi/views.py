from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from vcfapi.usecases import GetRecord, GetRecordList, DeleteRecord, InsertRecord, EditRecord, NotImplemented, RecordNotFound, OutOfLimits, BadParameters
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.parsers import JSONParser
from rest_framework_xml.parsers import XMLParser

# Create your views here.
class VCFView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [JSONRenderer, XMLRenderer]
    parser_classes = [JSONParser, XMLParser]
    def get(self, request: Request, *args, **kwargs):
        try:
            if request.query_params.get('id'):
                res = GetRecord(request).response
            elif (request.query_params.get('ofs') and request.query_params.get('size')) or (not request.query_params):
                res = GetRecordList(request).response
            else:
                return Response('Bad parameters', status=status.HTTP_400_BAD_REQUEST)
            return Response(res, status=status.HTTP_200_OK)
        except RecordNotFound as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        except NotImplemented as e:
            return Response(str(e), status=status.HTTP_501_NOT_IMPLEMENTED)
        except OutOfLimits as e:
            return Response(str(e), status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)
        except BadParameters as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request: Request, *args, **kwargs):
        try:
            res = InsertRecord(request).response
            return Response(None, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def put(self, request :Request, *args, **kwargs):
        try:
            if not request.query_params.get('id') or request.query_params.get('id') != request.data['ID']:
                return Response('No id or id is not matching record', status=status.HTTP_400_BAD_REQUEST)
            res = EditRecord(request).response
            return Response(None, status=status.HTTP_200_OK)
        except RecordNotFound as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request: Request, *args, **kwargs):
        try:
            if request.query_params.get('id'):
                res = DeleteRecord(request).response
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response('Bad parameters', status=status.HTTP_400_BAD_REQUEST)
        except RecordNotFound as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
