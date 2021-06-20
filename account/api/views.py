from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from account.api.serializers import RegistrationSerializer

@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}

    if serializer.is_valid():
        account = serializer.save()
        data['response'] = 'user registered successfully'
        data['username'] = account.username
        data['email'] = account.email
        return Response(data, status.HTTP_201_CREATED)
    else:
        data = serializer.errors
    
    return Response(data, status.HTTP_400_BAD_REQUEST)

