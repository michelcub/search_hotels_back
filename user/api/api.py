from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from user.api.serializer import UserSerializer
from django.contrib.auth.models import User


@api_view(['GET'])
def get_data_user(request, id):
    user = User.objects.get(pk=id)
    if not user:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    data = UserSerializer(user).data
    return Response(data, status=status.HTTP_200_OK)

