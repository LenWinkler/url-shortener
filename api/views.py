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
    hashed_url = hashlib.sha256(encoded_url).hexdigest()[:8]

    data_for_serializer = {
        raw = request.data['raw'],
        url_hash = hashed_url,
        short = fr'http://127.0.0.1:8000/api/{url_hash}'
    }

    serializer = UrlSerializer(data=data_for_serializer)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)