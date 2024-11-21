from asgiref.sync import sync_to_async
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import CommentForm, EditCommentForm
from .models import Comment, ArtPiece, Like
from .serializers import CommentSerializer


"""Comment functionality"""


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        art_piece_id = self.kwargs['art_piece_id']
        return Comment.objects.filter(art_piece_id=art_piece_id)

    def perform_create(self, serializer):
        art_piece = ArtPiece.objects.get(id=self.kwargs['art_piece_id'])
        serializer.save(user=self.request.user, art_piece=art_piece)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            print(response.data)
            return Response({
                'id': response.data['id'],
                'content': response.data['content'],
                'art_piece_id': self.kwargs['art_piece_id'],
                'timestamp': response.data.get('timestamp', None),
                'status': response.data.get('status', None),
            }, status=status.HTTP_201_CREATED)
        return response


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get(self, request, art_piece_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, art_piece_id=art_piece_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def post(self, request, art_piece_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, art_piece_id=art_piece_id)

        method = request.POST.get('method')
        if method == 'DELETE':
            comment.delete()
            return redirect('art_gallery_list')  # Redirect after deletion

        # Handle Update
        elif method == 'EDIT':
            serializer = CommentSerializer(comment, data=request.POST, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)  # Redirect after update
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


"""Like functionality"""


class LikeArtPieceView(APIView):
    def post(self, request, pk):
        try:
            art_piece = ArtPiece.objects.get(id=pk)
            user = request.user

            # Check if the user has already liked this art piece
            existing_like = Like.objects.filter(user=user, art_piece=art_piece).first()

            if existing_like:
                # If already liked, remove the like
                existing_like.delete()
                action = 'unliked'
            else:
                # If not liked yet, create a new like
                Like.objects.create(user=user, art_piece=art_piece)
                action = 'liked'

            # Get updated like count
            like_count = art_piece.likes_count()

            return Response({
                'success': True,
                'action': action,
                'like_count': like_count
            })

        except ArtPiece.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Art piece not found.'
            }, status=status.HTTP_404_NOT_FOUND)

