from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import response, decorators, permissions, status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

# Create your views here.

from .serializers import (
    Login_Serializer,
    Register_Serializer,
    Group_User_Serializer,

)


from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *

class Register_API(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = Register_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user =serializer.save()

        data = {
            "message":"Account registered successfully !"
        }

        return Response(data, status.HTTP_201_CREATED)


class Login_API(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = Login_Serializer

    def get_tokens_for_user(self, user):
        return RefreshToken.for_user(user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            if username is None or password is None:
                return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(username=username, password=password)
            if not user:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)

            refresh = self.get_tokens_for_user(user)

            groupquery = user.groups.all()
            serializerofgroup = Group_User_Serializer(groupquery, many=True)

            user_id = str(user.id)
            user_name = str(user.account.name)

            data = {
                'id':user_id,
                'name': user_name,
                'user_group': serializerofgroup.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(data, status=status.HTTP_201_CREATED)


from .serializers import MainUser_Serializer
class MainUser_API(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = MainUser_Serializer

    def get_queryset(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance= queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance = queryset, data=request.data,)
        if serializer.is_valid():
            serializer.save()
            return Response("success edited", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

from .serializers import ChangePassword_Serializer
class ChangePassword_API(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ChangePassword_Serializer

    def get_queryset(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance = queryset, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response("success changed password", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


from .serializers import MainAccount_Serializer
class MainAccount_API(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = MainAccount_Serializer

    def get_queryset(self):
        return get_object_or_404(Account, user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance= queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance = queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("success edited", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

from .serializers import MainProfile_Serializer
class MainProfile_API(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = MainProfile_Serializer

    def get_queryset(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance= queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance = queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("success edited", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


from .serializers import UserList_Serializer
from django.db.models import Q
class UserList_API(generics.GenericAPIView):
    serializer_class = UserList_Serializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if 'search' in self.request.query_params:
            finder = self.request.query_params['search']
            result = User.objects.filter(
                Q(account__name__icontains=finder) |
                Q(account__public_username__icontains=finder)
            )
            return result
        else:
            return User.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from .serializers import UserDetail_Serializer
class UserDetail_API(generics.GenericAPIView):
    serializer_class = UserDetail_Serializer
    permission_classes = [permissions.AllowAny,]


    def get_queryset(self):
        finder = ""
        if 'user_id' in self.kwargs:
            finder = self.kwargs['user_id']
            result = get_object_or_404(User, id=finder)
            return result
        elif 'user_pu' in self.kwargs:
            finder = self.kwargs['user_pu']
            result = get_object_or_404(User, account__public_username=finder)
            return result



    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




    # SendRequest_API,
    # CancelRequest_API,
    # Follow_API,
    # Unfollow_API,

from .serializers import MainRequest_Serializer
class MainRequest_API(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MainRequest_Serializer

    def get_queryset(self):
        return request.user.request_set.all().filter(status='pending')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MainRequest_Accept_API(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]    

    def get_queryset(self):
        finder = self.kwargs['request_id']
        return get_object_or_404(Request, id=finder)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.status = 'accepted'
        queryset.save()
        return Response("request accepted", status=status.HTTP_201_CREATED)
        
        

class MainRequest_Cancel_API(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]    

    def get_queryset(self):
        finder = self.kwargs['request_id']
        return get_object_or_404(Request, id=finder)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.status = 'cancelled'
        queryset.save()
        return Response("request cancelled", status=status.HTTP_201_CREATED)

    # MainRelationship_API,
    # MainFollow_API,
    # MainFollower_API,
from .serializers import MainRelationship_Serializer
class MainRelationship_API(generics.GenericAPIView):
    serializer_class = MainRelationship_Serializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        obj = Relationship.objects.get(user=request.user)
        return obj.connected_users.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

from .serializers import MainFollow_Serializer
class MainFollow_API(generics.GenericAPIView):
    serializer_class = MainFollow_Serializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return request.user.follow.to_user.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)




class SendRequest_API(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        finder = ""
        if 'user_id' in self.kwargs:
            finder = self.kwargs['user_id']
            result = get_object_or_404(User, id=finder)
            return result

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.user == queryset:
            return Response("cannot request its own user", status=status.HTTP_400_BAD_REQUEST)
        elif queryset.request_set.all().filter(from_user=request.user).exists():
            pass
        else:
            request = Request.objects.create(user=queryset,from_user=request.user,status='pending')
            request.save()
            return Response("request is created", status=status.HTTP_201_CREATED)
        
class CancelRequest_API(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        finder = ""
        if 'user_id' in self.kwargs:
            finder = self.kwargs['user_id']
            result = get_object_or_404(User, id=finder)
            return result

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.user == queryset:
            return Response("cannot request its own user", status=status.HTTP_400_BAD_REQUEST)
        elif queryset.request_set.all().filter(from_user=request.user).exists():
            obj = queryset.request_set.all().filter(from_user=request.user)
            obj.delete()
            return Response("request cancelled", status=status.HTTP_200_OK)
        else:
            return Response("no request can be cancelled", status=status.HTTP_400_BAD_REQUEST)

class Follow_API(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        finder = ""
        if 'user_id' in self.kwargs:
            finder = self.kwargs['user_id']
            result = get_object_or_404(User, id=finder)
            return result

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.user == queryset:
            return Response("cannot follow its own user", status=status.HTTP_400_BAD_REQUEST)
        else:
            # obj, created = Follow.objects.get_or_create(user=request.user,to_user=queryset)
            # obj.save()

            a = Follow.objects.get(user=request.user)
            if queryset in a.to_user.all():
                pass
            else:
                a.to_user.all().add(queryset)
                a.save()
            return Response("Success Following", status=status.HTTP_201_CREATED)
class Unfollow_API(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        finder = ""
        if 'user_id' in self.kwargs:
            finder = self.kwargs['user_id']
            result = get_object_or_404(User, id=finder)
            return result

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.user == queryset:
            return Response("cannot unfollow its own user", status=status.HTTP_400_BAD_REQUEST)
        else:   
            obj = request.user.follow.all().filter(to_user=queryset)
            if obj.exists():
                obj.delete()
                return Response("success unfollow the user",status=status.HTTP_201_CREATED)
            else:
                return Response("you did not follow the user",status=status.HTTP_400_BAD_REQUEST)    


from .serializers import PostList_S
from .serializers import PostList_returnDetailLink_S
from .helpers import SmallResultsSetPagination
class PostList_API(generics.GenericAPIView):
    serializer_class = PostList_S
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        if 'user_id' in self.kwargs:
            return Post.objects.all().filter(poster=self.kwargs['user_id'])
        elif not self.request.query_params:
            return Post.objects.all()
        else:
            search = ""
            if 'search' in self.request.query_params:
                search = self.request.query_params['search']
            # friend_only = self.request.query_params['friend_only']
            # likes = self.request.query_params['likes']
            # tags = self.request.query_params['tags']
            result = Post.objects.all().filter(
                Q(title__icontains=search) |
                Q(text__icontains=search)  
            )
            return result


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PostList_returnDetailLink_S(queryset, many=True ,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response("success", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .serializers import PostDetail_S
from .serializers import PostDetail_notOwner_S
class PostDetail_API(generics.GenericAPIView):
    serializer_class = PostDetail_S
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # return get_object_or_404(Post, id=self.kwargs['post_id'])
        return get_object_or_404(Post, id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if request.user.id is None:
            return Response("cant update, must logged in", status=status.HTTP_401_UNAUTHORIZED)
        #owner of post
        elif queryset.poster == request.user:
            #   bisa edit title text likebutton dengan PostDetaiL_S serializer
            serializer = PostDetail_S(instance=queryset, data=request.data)
            if serializer.is_valid():

                ################ LIKES BUTTON HANDLER ###################

                # probably there is a lot of ways to create a custom serializer and deserializer an object
                # we are trying to make the like (manytomanyfield) in Post to have an handler such as button like !
                # the first solution came up was using SerializerMethodField (but unfortunately it is read-only field , can't be read when deserializing)
                # and there are also ways to do so by using our own creatad field such as writableMethodField using to_representation or to_internal_value , but we cover it later
                # right now we are using a "source" technique passed in serializer.booleanField of serializer PostDetail_S that tells does authenticated user like the post already or not
                # don't forget to specify required=False in the serializer field too , so it won't thrown an error when the request.body doesn't have the "likebutton" data
                # the problem is , written as below
                
                # if (source="") is used in serializer , which we used source as "does_authenticated_user_like" (located in Models.py)
                # so the name of field in validated_data (which is supposed to be likebutton) is equal to the name of the given source
                # there is no serializer.validated_data['likebutton], but there is serializer.validated_data['does_authenticated_user_like'] instead
                
                # for i in serializer.validated_data:
                #     print("data is "+i)

                # example of the body request is given as below
                # {
                #     "title":"changed3",
                #     "text":"changed3",
                #     "likebutton":false
                # }

                # this will print
                #   data is title
                #   data is text
                #   data is does_authenticated_user_like

                # if in the request body API is given a "likebutton":true or "likebutton":false
                # the serializer.save() will throw an error of "cant set attribute" because it can't handdle what to do with the field named "does_authenticated_user_like" in it's serializer.validated_data
                # the error of "can't set attribute" is catched while doing serializer.save() 

                # so we must take this action by ourself
                # and we have to delete the 'does_authenticated_user_like' in validated_data before jump into serializer.save() as we no longer need it anymore because we handled the action
                
                if 'does_authenticated_user_like' in serializer.validated_data:
                    # we collect the data first into variable
                    likebutton = serializer.validated_data['does_authenticated_user_like']
                    # and then we can delete it so it won't throw an error while calling serializer.save() and also it is no longer needed
                    del serializer.validated_data['does_authenticated_user_like']

                    if request.user in queryset.likes.all():
                        if likebutton == True:
                            pass
                        else:
                            queryset.likes.remove(request.user)
                            queryset.save()
                    else:
                        if likebutton == True:
                            queryset.likes.add(request.user)
                            queryset.save()
                        else:
                            pass

                ################ LIKES BUTTON HANDLER ###################

                serializer.save()
                return Response("updated", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #not owner of post
        else:          
            #   bisa edit likebutton dengan PostDetail_notOwner_S serializer 
            serializer = PostDetail_notOwner_S(instance=queryset, data=request.data)
            if serializer.is_valid():
                ################ LIKES BUTTON HANDLER ###################
                if 'does_authenticated_user_like' in serializer.validated_data:
                    # we collect the data first into variable
                    likebutton = serializer.validated_data['does_authenticated_user_like']
                    # and then we can delete it so it won't throw an error while calling serializer.save()
                    del serializer.validated_data['does_authenticated_user_like']

                    if request.user in queryset.likes.all():
                        if likebutton == True:
                            pass
                        else:
                            queryset.likes.remove(request.user)
                            queryset.save()
                    else:
                        if likebutton == True:
                            queryset.likes.add(request.user)
                            queryset.save()
                        else:
                            pass
                ################ LIKES BUTTON HANDLER ###################

                serializer.save()
                return Response("updated", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # if the logged in user is owner of post , can delete
        if queryset.poster == request.user:
            queryset.delete()
            return Response("deleted", status=status.HTTP_201_CREATED)
        # otherwise , can't
        else:
            return Response("must be authorized or the owner of post", status=status.HTTP_401_UNAUTHORIZED)

from .serializers import PostLikes_Serializer
class PostLikes_API(generics.GenericAPIView):
    serializer_class = PostLikes_Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        a = get_object_or_404(Post, id=self.kwargs['pk'])
        return a.likes.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


from .serializers import PostPhotoList_S
class PostPhotoList_API(generics.GenericAPIView):
    serializer_class = PostPhotoList_S
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    

    def get_queryset(self):
        return get_list_or_404(PostPhoto, post__id=self.kwargs['post_id'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.post.poster == request.user:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(post=Post.objects.get(id=self.kwargs['post_id']))
                return Response("success added photo to a post", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("only poster can add photo the the post", status=status.HTTP_401_UNAUTHORIZED)

from .serializers import PostPhotoDetail_S
class PostPhotoDetail_API(generics.GenericAPIView):
    serializer_class = PostPhotoDetail_S
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        return get_object_or_404(PostPhoto, id=self.kwargs['postphoto_id'])
    
    def get(self, request, *args, **kwargs):
        queryset=  self.get_queryset()
        serializer = self.get_serializer(instance= queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        queryset=  self.get_queryset()
        if queryset.post.poster == request.user:
            serializer = self.get_serializer(instance= queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("success edit", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("only poster can edit the photo", status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, *args, **kwargs):
        queryset=  self.get_queryset()
        if queryset.post.poster == request.user:
            queryset.delete()
            return Response("photo is deleted", status=status.HTTP_200_OK)
        else:
            return Response("only poster can delete photo", status=status.HTTP_401_UNAUTHORIZED)

        




    





from .serializers import CommentList_S
from .serializers import CommentList_returnDetailLink_S
class CommentList_API(generics.GenericAPIView):
    serializer_class = CommentList_S
    permission_classes = [permissions.AllowAny]
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        return get_list_or_404(Comment, post__id=self.kwargs['post_id'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommentList_returnDetailLink_S(instance = queryset, many=True,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self ,request, *args, **kwargs):
        if request.user.id is None:
            return Response("must be authoriezed to create a comment", status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    post=Post.objects.get(id=self.kwargs['id']),
                    commentator=request.user
                    )
                return Response("success create a comment", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .serializers import CommentDetail_S
from .serializers import CommentDetail_notOwner_S
class CommentDetail_API(generics.GenericAPIView):
    serializer_class = CommentDetail_S
    permission_classes = [permissions.AllowAny]
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        return get_object_or_404(Comment, id=self.kwargs['comment_id'])
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance = queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if request.user.id is None:
            return Response("cant update, must logged in", status=status.HTTP_401_UNAUTHORIZED)
        elif queryset.commentator == request.user:
            serializer = CommentDetail_S(instance = queryset, data=request.data)
            if serializer.is_valid():

                ######## LIKES BUTTON HANDLER ########
                if 'does_authenticated_user_like' in serializer.validated_data:
                    # we collect the data first into variable
                    likebutton = serializer.validated_data['does_authenticated_user_like']
                    # and then we can delete it so it won't throw an error while calling serializer.save() and also it is no longer needed
                    del serializer.validated_data['does_authenticated_user_like']

                    if request.user in queryset.likes.all():
                        if likebutton == True:
                            pass
                        else:
                            queryset.likes.remove(request.user)
                            queryset.save()
                    else:
                        if likebutton == True:
                            queryset.likes.add(request.user)
                            queryset.save()
                        else:
                            pass
                #######################################
                serializer.save()
                return Response("updated", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CommentDetail_notOwner_S(instance=queryset, data=request.data)
            if serializer.is_valid():
                
                ######## LIKES BUTTON HANDLER ########
                if 'does_authenticated_user_like' in serializer.validated_data:
                    # we collect the data first into variable
                    likebutton = serializer.validated_data['does_authenticated_user_like']
                    # and then we can delete it so it won't throw an error while calling serializer.save() and also it is no longer needed
                    del serializer.validated_data['does_authenticated_user_like']

                    if request.user in queryset.likes.all():
                        if likebutton == True:
                            pass
                        else:
                            queryset.likes.remove(request.user)
                            queryset.save()
                    else:
                        if likebutton == True:
                            queryset.likes.add(request.user)
                            queryset.save()
                        else:
                            pass
                #####################################
                serializer.save()
                return Response("updated", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                


    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.commentator == request.user:
            queryset.delete()
            return Response("deleted", status=status.HTTP_200_OK)
        else:
            return Response("only authorized owner of the comment is allowed", status=status.HTTP_401_UNAUTHORIZED)








from .serializers import PhotoList_S
class PhotoList_API(generics.GenericAPIView):
    serializer_class = PhotoList_S
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        if 'user_id' in self.kwargs:
            return Photo.objects.all().filter(user=self.kwargs['user_id'])
        else:
            return Photo.objects.all()

    def get(self, request, *args, **kwrags):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance= queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response("success created", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .serializers import PhotoDetail_S
from .serializers import PhotoDetail_notOwner_S
class PhotoDetail_API(generics.GenericAPIView):
    serialier_class = PhotoDetail_S
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        return get_object_or_404(Photo, id=self.kwargs['photo_id'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset.user == request.user:
            serializer = PhotoDetail_S(instance = queryset, data=request.data)
            if serializer.is_valid():

                ########################
                if 'does_authenticated_user_like' in serializer.validated_data:
                    # we collect the data first into variable
                    likebutton = serializer.validated_data['does_authenticated_user_like']
                    # and then we can delete it so it won't throw an error while calling serializer.save() and also it is no longer needed
                    del serializer.validated_data['does_authenticated_user_like']

                    if request.user in queryset.likes.all():
                        if likebutton == True:
                            pass
                        else:
                            queryset.likes.remove(request.user)
                            queryset.save()
                    else:
                        if likebutton == True:
                            queryset.likes.add(request.user)
                            queryset.save()
                        else:
                            pass
                ########################

                serializer.save()
                return Response("success edited", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.PhotoDetail_notOwner_S(instance = queryset, data=request.data)
            if serializer.is_valid():

                ########################
                if 'does_authenticated_user_like' in serializer.validated_data:
                    # we collect the data first into variable
                    likebutton = serializer.validated_data['does_authenticated_user_like']
                    # and then we can delete it so it won't throw an error while calling serializer.save() and also it is no longer needed
                    del serializer.validated_data['does_authenticated_user_like']

                    if request.user in queryset.likes.all():
                        if likebutton == True:
                            pass
                        else:
                            queryset.likes.remove(request.user)
                            queryset.save()
                    else:
                        if likebutton == True:
                            queryset.likes.add(request.user)
                            queryset.save()
                        else:
                            pass
                ########################

                serializer.save()
                return Response("success edited", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # if the logged in user is owner of photo , can delete
        if queryset.user == request.user:
            queryset.delete()
            return Response("deleted", status=status.HTTP_201_CREATED)
        # otherwise , can't
        else:
            return Response("must be authorized or the owner of post", status=status.HTTP_401_UNAUTHORIZED)


from .serializers import PhotoCommentList_S
class PhotoCommentList_API(generics.GenericAPIView):
    serializer_class = PhotoCommentList_S
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        return get_list_or_404(PhotoComment, photo__id=self.kwargs['photo_id'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance = queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self ,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                photo = Photo.objects.get(id=self.kwargs['photo_id']),
                commentator=request.user
                )
            return Response("success create a comment", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .serializers import PhotoCommentDetaiL_S
from .serializers import PhotoCommentDetail_notOwner_S
class PhotoCommentDetail_API(generics.GenericAPIView):
    serializer_class = PhotoCommentDetaiL_S
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        return get_object_or_404(PhotoComment, id=self.kwargs['photocomment_id'])
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance = queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.commentator == request.user:
            serializer = PhotoCommentDetaiL_S(instance = queryset, data=request.data)
            if serializer.is_valid():

                ######## LIKES BUTTON HANDLER ########
                if 'does_authenticated_user_like' in serializer.validated_data:
                    # we collect the data first into variable
                    likebutton = serializer.validated_data['does_authenticated_user_like']
                    # and then we can delete it so it won't throw an error while calling serializer.save() and also it is no longer needed
                    del serializer.validated_data['does_authenticated_user_like']

                    if request.user in queryset.likes.all():
                        if likebutton == True:
                            pass
                        else:
                            queryset.likes.remove(request.user)
                            queryset.save()
                    else:
                        if likebutton == True:
                            queryset.likes.add(request.user)
                            queryset.save()
                        else:
                            pass
                #######################################
                serializer.save()
                return Response("updated", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PhotoCommentDetaiL_notOwner_S(instance=queryset, data=request.data)
            if serializer.is_valid():
                
                ######## LIKES BUTTON HANDLER ########
                if 'does_authenticated_user_like' in serializer.validated_data:
                    # we collect the data first into variable
                    likebutton = serializer.validated_data['does_authenticated_user_like']
                    # and then we can delete it so it won't throw an error while calling serializer.save() and also it is no longer needed
                    del serializer.validated_data['does_authenticated_user_like']

                    if request.user in queryset.likes.all():
                        if likebutton == True:
                            pass
                        else:
                            queryset.likes.remove(request.user)
                            queryset.save()
                    else:
                        if likebutton == True:
                            queryset.likes.add(request.user)
                            queryset.save()
                        else:
                            pass
                #####################################
                serializer.save()
                return Response("updated", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                





from .serializers import T_PostList_S
class T_PostList_API(generics.GenericAPIView):
    serializer_class = T_PostList_S
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        if 'user_id' in self.kwargs:
            return Post.objects.all().filter(poster=self.kwargs['user_id'])
        elif not self.request.query_params:
            return Post.objects.all()
        else:
            search = ""
            if 'search' in self.request.query_params:
                search = self.request.query_params['search']
            # friend_only = self.request.query_params['friend_only']
            # likes = self.request.query_params['likes']
            # tags = self.request.query_params['tags']
            result = Post.objects.all().filter(
                Q(title__icontains=search) |
                Q(text__icontains=search)  
            )
            return result


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response("success", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from .serializers import T_CommentList_S
# class T_CommentList_API(generics.GenericAPIView):
#     serializer_class = T_CommentList_S
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get_queryset(self):
#         return get_list_or_404(Comment, post__id=self.kwargs['post_id'])

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(instance = queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self ,request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, context={
#             'request':request
#             })
#         if serializer.is_valid():
#             serializer.save()
#             return Response("success create a comment", status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		