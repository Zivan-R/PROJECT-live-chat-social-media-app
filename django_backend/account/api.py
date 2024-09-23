from django.http import JsonResponse

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .forms import SignupForm

@api_view(['GET'])
def me(request):
    print('request data me', request.data)
    
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
    })

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def signup(request):
    data = request.data
    
    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })
    
    if form.is_valid():
        form.save()
        
        return Response({'message': 'user created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'error', 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)