import hashlib
import re

from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .hash_checker import url_hash_exists
from .models import Url
from .serializers import UrlSerializer

@api_view(['GET'])
def retrieve_url(request, existing_hash):
    url_is_valid = url_hash_exists(existing_hash)
    if url_is_valid:
        serializer = UrlSerializer(url_is_valid)
        return redirect(serializer.data['raw'], permanent=True)
    
    return Response(
        {'Error':'Url not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST', 'GET'])
def create_url(request):
    try: # check to make sure 'raw' key is in req body
        serializer_data = {
            'raw': request.data['raw'],
            'url_hash': '',
            'short': ''
        }

        try: # if user passed a custom url in the request body
            custom_url = request.data['custom']

            if not re.search(r'^[a-zA-Z0-9]{3,8}$', custom_url):
                return Response(
                    {
                        'Error': 'Url must use only alphanumeric chars and' \
                                 'must be between 3-8 chars'
                    },
                    status=status.HTTP_400_BAD_REQUEST)

            custom_hash_already_exists = url_hash_exists(custom_url)
            if custom_hash_already_exists:
                return Response(
                    {'Error': 'This url is already taken'},
                    status=status.HTTP_409_CONFLICT)

            serializer_data['url_hash'] = custom_url
            serializer_data['short'] = (f'''https://shortn-it.herokuapp.com'''
                                        f'''/{custom_url}/''')
            serializer = UrlSerializer(data=serializer_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 
                                status=status.HTTP_201_CREATED)

            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except: # if no custom url was passed
            encoded_url = request.data['raw'].encode('utf-8')
            hashed_url = hashlib.sha256(encoded_url).hexdigest()[:8]

            already_exists = url_hash_exists(hashed_url)
            if already_exists:
                serializer = UrlSerializer(already_exists)
                return Response(
                    {'already_exists': f'{serializer.data["short"]}'},
                    status=status.HTTP_200_OK)

            serializer_data['url_hash'] = hashed_url
            serializer_data['short'] = (f'''https://shortn-it.herokuapp.com'''
                                        f'''/{hashed_url}/''')
            serializer = UrlSerializer(data=serializer_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)

            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response(
                        {"Error": "Missing 'raw' key in body of request"},
                        status=status.HTTP_400_BAD_REQUEST)
