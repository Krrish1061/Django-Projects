from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from blogpost.models import Post
from .serializers import PostSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/blogpost'},
        {'GET': '/api/single-blogpost/id'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},

    ]

    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blogpost(request):
    post = Post.objects.all()
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_blogpost(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)
