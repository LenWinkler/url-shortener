import hashlib
import re

from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from url.hash_checker import url_hash_exists
from url.models import Url
from url.serializers import UrlSerializer


@api_view(['GET'])
def retrieve_url(request, existing_hash):
    url_is_valid = url_hash_exists(existing_hash)
    if url_is_valid:
        serializer = UrlSerializer(url_is_valid)
        return redirect(serializer.data['raw'], permanent=True)
    
    return Response(
        {'Error':'Url not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_url(request):
    if not 'raw' in request.data:
        return Response(
                        {"Error": "Missing 'raw' key in body of request"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer_data = {
            'raw': request.data['raw'],
            'url_hash': '',
            'short': ''
        }
        if 'custom' in request.data:
            if not re.search(r'^[a-zA-Z0-9]{3,8}$', request.data['custom']):
                return Response(
                    {
                        'Error': ('Url must use only alphanumeric chars and'
                                  'must be between 3-8 chars')
                    },
                    status=status.HTTP_400_BAD_REQUEST)
            serializer_data['url_hash'] = request.data['custom']
        else:
            encoded_url = request.data['raw'].encode('utf-8')
            hashed_url = hashlib.sha256(encoded_url).hexdigest()[:8]
            serializer_data['url_hash'] = hashed_url

        if url_hash_exists(serializer_data['url_hash']):
            return Response(
                    {'Error': 'This url is already taken'},
                    status=status.HTTP_409_CONFLICT)

        serializer_data['short'] = ('https://shortn-it.herokuapp.com'
                                    f'/{serializer_data["url_hash"]}/')

        serializer = UrlSerializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)
