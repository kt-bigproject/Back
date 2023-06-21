from .models import Blog, Comment
from .serializer import BlogSerializer, CommentSerializer
from rest_framework import viewsets
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.pagination import PageNumberPagination

# (게시글) Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
class BlogViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JSONWebTokenAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Blog.objects.all().order_by('-created_at')
    pagination_class = PageNumberPagination
    serializer_class = BlogSerializer
   
    # def perform_create(self, serializer):
    #     serializer.save(user = self.request.user)

# (댓글) Comment 보여주기, 수정하기, 삭제하기 모두 가능
class CommentViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JSONWebTokenAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blog']

    # def perform_create(self, serializer):
    #     serializer.save(user = self.request.user)