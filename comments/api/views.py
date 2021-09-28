from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from comments.models import Comment
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
    CommentSerializerForUpdate,
)
from comments.api.permissions import IsObjectOwner  # authentication

class CommentViewSet(viewsets.GenericViewSet):
    """
    only support list, create, update and delete method. You can implement retrieve by yourself
    """
    serializer_class = CommentSerializerForCreate
    queryset = Comment.objects.all()
    filterset_fields = ("tweet_id",)

    def get_permissions(self):
        # we should use AllowAny() rather than AllowAny because we want to create an instance
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['destroy', 'update']:
            return [IsAuthenticated(), IsObjectOwner()] # destroy and update need to be authenticated and check owner
        return [AllowAny()]

    def list(self, request, *args, **kwargs):
        if 'tweet_id' not in request.query_params:
            return Response({
                'message': 'missing tweet_it in request',
                'success': False,
            }, status=status.HTTP_400_BAD_REQUEST,)
        queryset = self.get_queryset()
        comments = self.filter_queryset(queryset).order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response({
            'comments': serializer.data
        }, status=status.HTTP_200_OK,)

    def create(self, request, *args, **kwargs):
        data = {
            'user_id': request.user.id,
            'tweet_id': request.data.get('tweet_id'),
            'content': request.data.get('content'),
        }
        # the first default value was instance, we should parse the data by parsing it by parameters
        serializer = CommentSerializerForCreate(data=data)
        if not serializer.is_valid():
            return Response({
                'message' : 'Please check input',
                'errors' :  serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        # save method will trigger the create method inside serializer
        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        # get_object is a wrapper class of DRF, it will raise 404 error when we find nothing
        serializer = CommentSerializerForUpdate(
            instance=self.get_object(),
            data=request.data,
        )
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        # The destroy method will result to 204 no content, I will return 200 here, it is easy to understand
        # and straightforward
        return Response({'success':True}, status=status.HTTP_200_OK)

