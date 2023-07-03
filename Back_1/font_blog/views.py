from .models import Blog, Comment
from .serializer import BlogSerializer, CommentSerializer
from rest_framework import viewsets
from django.db.models import Count, Case, When, Value, IntegerField, F
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10

# (게시글) Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
class BlogViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdminUserOrReadOnly, IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsAdminUserOrReadOnly]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # queryset = Blog.objects.all().order_by('-radio_field','-created_at')
    queryset = Blog.objects.annotate(
        num_comments=Count('comment'),
        custom_order=Case(
            When(radio_field='announcement', then=Value(0)),
            default=Value(1),
            output_field=IntegerField(),
        ),
    ).order_by('custom_order', '-created_at')
    serializer_class = BlogSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = F('views') + 1  
        instance.save() 
        instance.refresh_from_db() 
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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

    def list(self, request):
        # parent 필드가 null인 댓글만 선택합니다.
        blog_id = request.query_params.get('blog', None)
        if blog_id is not None:
            comments = Comment.objects.filter(parent=None, blog=blog_id)
        else:
            comments = Comment.objects.filter(parent=None)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)