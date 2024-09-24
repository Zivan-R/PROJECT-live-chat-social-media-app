from django.http import JsonResponse

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .forms import SignupForm
from .models import FriendshipRequest, User
from .serializers import UserSerializer, FriendshipRequestSerializer

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

@api_view(["GET"])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []
    
    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)    # status makes it that only requests with status "sent" are showing
    
    friends = user.friends.all()
    
    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': FriendshipRequestSerializer(requests, many=True).data
    }, safe=False)
    
@api_view(['POST'])
def send_friendship_request(request, pk): 
    user = User.objects.get(pk=pk)
    
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)    # Check for you
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)    #check other way around
    
    if not check1 or not check2:
        friendship_request = FriendshipRequest.objects.create(created_for=user, created_by=request.user)
    
        return JsonResponse({'user': UserSerializer(user).data, 'message': 'Friendship request created'})   # Vue was throwing an error because user wasn't sent. 
    else:
        return JsonResponse({'user': UserSerializer(user).data, 'message': 'request already sent'})
    
@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    
    friendship_request.save()
    
    if friendship_request.status == 'accepted':
        user.friends.add(request.user)
        user.friends_count += 1
        user.save()
        
        request_user = request.user
        request_user.friends_count += 1
        request_user.save()
        
        # Made this to match requests, but maybe unecessary
        # if FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user):
        #     reverse_friendship_request = FriendshipRequest.objects.filter(created_for=user).get(created_by=request.user)
        #     reverse_friendship_request.status = status
            
    
    return JsonResponse({'message': 'Friendship request updated'})