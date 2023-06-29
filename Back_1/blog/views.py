from .models import Blog, Comment
from .serializer import BlogSerializer, CommentSerializer
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from django.db.models import Count, F
from rest_framework.decorators import action
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 8
    
# (게시글) Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
class BlogViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdminUserOrReadOnly, IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsAdminUserOrReadOnly]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.annotate(
        num_comments=Count('comment', distinct=True),
        num_likes=Count('likes', distinct=True)  
    ).order_by('-created_at')
    serializer_class = BlogSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        blog = self.get_object()
        blog.likes.add(request.user)
        return Response({'status': 'like set'})

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        blog = self.get_object()
        blog.likes.remove(request.user)
        return Response({'status': 'like unset'})
    
    @action(detail=True, methods=['POST'])
    def increase_views(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = F('views') + 1  
        instance.save(update_fields=['views'])
        return Response({'status': 'views increased'})
    
    @action(detail=True, methods=['GET'])
    def is_liked(self, request, pk=None):
        blog = self.get_object()
        user = request.user
        is_liked = blog.likes.filter(id=user.id).exists()
        return Response({'is_liked': is_liked})

# (댓글) Comment 보여주기, 수정하기, 삭제하기 모두 가능
class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdminUserOrReadOnly, IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsAdminUserOrReadOnly]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blog']

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)