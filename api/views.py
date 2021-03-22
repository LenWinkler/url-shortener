from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import hashlib
import re
from .serializers import UrlSerializer
from .hash_checker import url_hash_exists
from .models import Url

@api_view(['GET'])
def api_info(request):
    return Response(
        {"GET '/'": "returns info about api",
         "POST '/'": "create url. req body --> {'raw':'<full url>', 'custom'(optional):'<custom url>'}",
         "GET '/<existing url>/": "if url is valid, will redirect to the full length url"
        })

@api_view(['GET'])
def retrieve_url(request, existing_hash):
    url_is_valid = url_hash_exists(existing_hash)
    if url_is_valid:
        serializer = UrlSerializer(url_is_valid)
        return redirect(serializer.data['raw'])
    
    return Response({'Error':'Url not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_url(request):
    data_for_serializer = {
        'raw': request.data['raw'],
        'url_hash': '',
        'short': ''
    }

    try: # if user passed a custom url in the request body
        custom_url = request.data['custom']

        if not re.search(r'^[a-zA-Z0-9]{3,8}$', custom_url):
            return Response(
                {'Error': 'Url can only contain alphanumeric chars and must be between 3-8 chars long'},
                 status=status.HTTP_400_BAD_REQUEST)

        custom_hash_already_exists = url_hash_exists(custom_url)
        if custom_hash_already_exists:
            return Response({'Error': 'This url is already taken'}, status=status.HTTP_409_CONFLICT)

        data_for_serializer['url_hash'] = custom_url
        data_for_serializer['short'] = f'http://127.0.0.1:8000/{custom_url}/'
        serializer = UrlSerializer(data=data_for_serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except: # if no custom url was passed
        encoded_url = request.data['raw'].encode('utf-8')
        hashed_url = hashlib.sha256(encoded_url).hexdigest()[:8]

        already_exists = url_hash_exists(hashed_url)
        if already_exists:
            serializer = UrlSerializer(already_exists)
            return Response({'already_exists': f'{serializer.data["short"]}'}, status=status.HTTP_200_OK)

        data_for_serializer['url_hash'] = hashed_url
        data_for_serializer['short'] = f'http://127.0.0.1:8000/{hashed_url}/'
        serializer = UrlSerializer(data=data_for_serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)