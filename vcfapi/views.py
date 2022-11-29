from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from vcfapi.usecases import GetRecord, GetRecordList, DeleteRecord, InsertRecord, NotImplemented, RecordNotFound, OutOfLimits
from rest_framework import status

# Create your views here.
class VCFView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request , *args, **kwargs):
        try:
            if request.query_params.get('id'):
                id = request.query_params.get('id')
                res = GetRecord(id).response
            elif (request.query_params.get('ofs') and request.query_params.get('size')) or (not request.query_params):
                ofs = int(request.query_params.get('ofs')) if request.query_params.get('ofs') else 0
                size = int(request.query_params.get('size')) if request.query_params.get('size') else 10

                if ofs < 0 or size < 1:
                    return Response('Bad parameters', status=status.HTTP_400_BAD_REQUEST)
                
                res = GetRecordList(ofs, size).response
            else:
                return Response('Bad parameters', status=status.HTTP_400_BAD_REQUEST)

            return Response(res, status=status.HTTP_200_OK)
        except RecordNotFound as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        except NotImplemented as e:
            return Response(str(e), status=status.HTTP_501_NOT_IMPLEMENTED)
        except OutOfLimits as e:
            return Response(str(e), status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request: Request, *args, **kwargs):
        try:
            print (request.data)
            res = InsertRecord(request.data).response
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def put(self, request, *args, **kwargs):
        return Response({"msg" : "ok"})
    
    def delete(self, request, *args, **kwargs):
        try:
            if request.query_params.get('id'):
                id = request.query_params.get('id')
                res = DeleteRecord(id).response
                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response('Bad parameters', status=status.HTTP_400_BAD_REQUEST)
        except RecordNotFound as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
