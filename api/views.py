from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import hashlib
from .serializers import UrlSerializer
from .hash_checker import url_hash_exists

@api_view(['GET'])
def index(request):
    return Response('api is up')

@api_view(['POST'])
def create(request):
    encoded_url = request.data['raw'].encode('utf-8')
    hashed_url = hashlib.sha256(encoded_url).hexdigest()[:8]
    
    already_exists = url_hash_exists(hashed_url)
    if already_exists:
        serializer = UrlSerializer(already_exists)  
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    data_for_serializer = {
        'raw': request.data['raw'],
        'url_hash': hashed_url,
        'short': fr'http://127.0.0.1:8000/{hashed_url}'
    }

    serializer = UrlSerializer(data=data_for_serializer)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)