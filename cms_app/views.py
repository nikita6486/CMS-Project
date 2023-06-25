from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,GenericAPIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer, LikeSerializer, UserUpdateSerializer
# Create your views here.
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from datetime import datetime, timedelta, timezone


'''BY NIKITA: 
FIRST IS THE SIMPLEST WAY WE CAN HANDLE CRUD OPERATION USING DJANGO, OTHER WAY IS SHOWN FOR USERS CRUD OPERATION
On every post you will get number of likes also'''
# 1======================================================================
# class UserListCreateAPIView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the instance of the post/blog
        pk = kwargs.get('pk')
        
        if pk is not None:
            instance = self.get_object()

            # Check if the post/blog is public or owned by the current user for perticular post
            if instance.is_public or (request.user.is_authenticated and instance.owner == request.user):
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                return Response(data={"Status": status.HTTP_403_FORBIDDEN,
                                    "Message": "Access denied."},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            queryset = self.filter_queryset(self.get_queryset())

            # Check if the post/blog is public or owned by the current user for all posts
            queryset = queryset.filter(is_public=True) | queryset.filter(owner=request.user)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Check if the authenticated user is the owner of the post
        if instance.owner != request.user:
            return Response(data={"message": "You are not allowed to update this post."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    
    def delete(self, request, pk,*args, **kwargs):
        post_id = pk
        # Retrieve the post instance using a query
        try:
            instance = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response(data={"message": "Post not found."},
                            status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the owner of the post
        if instance.owner != request.user:
            return Response(data={"message": "You are not allowed to delete this post."},
                            status=status.HTTP_403_FORBIDDEN)

        instance.delete()

        return Response(data={"message": "Your Post is deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)

class LikeCreateAPIView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]


"""2============================================================================================
Here is the other ways we can give api access seperately CRUD operation SHOWN on User table, same way we can also do for POST and LIKE tables"""
class UserListCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                  "Message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=serializer.validated_data['email'], deleted_at__isnull=True).exists():
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                  "Message": "User Email Already Registered",},
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                serializer.save()
                return Response(data={"Status": status.HTTP_201_CREATED,
                                      "Message": "User Registered",
                                      "Results": serializer.data},
                                status=status.HTTP_201_CREATED)
            except:
                return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                      "Message": serializer.errors},
                                status=status.HTTP_201_CREATED)


# Anyone can access Userlist:
class UserListAPIView(ListAPIView):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(),many=True)
        if serializer.data == []:
            return Response(data={"Message":"List of Users is Empty"},
                            status=status.HTTP_204_NO_CONTENT)

        return Response(data={"Message":"List of user",
                               "Results": serializer.data},
                        status=status.HTTP_200_OK)
    
# Only authorised user can update user:    
class UpdateUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer
    
    def put(self,request,*args, **kwargs):
        user = request.user
        if not User.objects.filter(id=user.id):
            return Response(data={"Status": status.HTTP_404_NOT_FOUND,
                                  "Message": "User ID not found"},
                            status=status.HTTP_404_NOT_FOUND)
        user=User.objects.get(id=user.id)

        serializer = UserUpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data={"Status": status.HTTP_200_OK,
                                  "Message": "User data updated successfully",
                             "Results": serializer.data},
                            status= status.HTTP_200_OK)
        return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                              "Message": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
    

# Only authorised user can delete user:    
class DeleteUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        user = request.user
        if not User.objects.filter(id=user.id):
            return Response(data={"Status": status.HTTP_404_NOT_FOUND,
                                  "Message": 'User is not found'},
                            status=status.HTTP_404_NOT_FOUND)
        
        deleted_at = datetime.utcnow().replace(tzinfo=timezone.utc)
        User.objects.filter(id=user.id).update(deleted_at=deleted_at,is_active=False)
        return Response(data={"Status": status.HTTP_204_NO_CONTENT,
                              "Message": 'User Account is deleted successfully'},
                        status=status.HTTP_200_OK)