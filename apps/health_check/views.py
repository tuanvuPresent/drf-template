from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(methods=['get'], tags=['default'])
@api_view(['GET'])
def ping(request):
    return Response('pong')
