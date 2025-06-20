from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer

from .forms import PostForm
from .models import Post, Like, Comment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer

@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    
    return JsonResponse({
        'post': PostDetailSerializer(post).data,
    })

@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    
    posts = Post.objects.filter(created_by_id=id)
    
    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    
    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data
    }, safe=False)

@api_view(['POST'])
def post_create(request):
    # data = request.data
    form = PostForm(request.data)
    
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user  # added automatically since we're authenticated
        post.save()
        
        serializer = PostSerializer(post,)
        
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'help!'})
    
@api_view(['POST'])
def post_like(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    
    
    if not post.likes.filter(created_by=request.user).exists():
        like = Like.objects.create(created_by=request.user)
        post.likes_count += 1
        post.likes.add(like)
        post.save()
    
        return JsonResponse({'message': 'like created'})
    else:
        return JsonResponse({'message': 'post already liked'})
    
@api_view(['POST'])
def post_create_comment(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)
    
    post.comments.add(comment)
    post.comments_count += 1
    post.save()
    
    serializer = CommentSerializer(comment)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'message': 'Error, post not found'})
    
    post.delete()
    
    return JsonResponse({'message': 'post deleted'})
    