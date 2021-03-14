from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import hashlib
from .serializers import UrlSerializer

@api_view(['GET'])
def index(request):
    return Response('api is up')

@api_view(['POST'])
def create(request):
    encoded_url = request.data['raw_url'].encode('utf-8')
    url_hash = hashlib.sha256(encoded_url).hexdigest()[:8]

    response = {
        request.data['raw_url'],
        url_hash
    }

    return Response(response)