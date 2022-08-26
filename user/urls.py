from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from .views import (
    Register_API,
    Login_API,

    MainUser_API,
    ChangePassword_API,
    MainAccount_API,
    MainProfile_API,

    UserList_API,
    UserDetail_API,

    MainRequest_API,
    MainRequest_Accept_API,
    MainRequest_Cancel_API,
    MainRelationship_API,
    MainFollow_API,
    # MainFollower_API,
    
    SendRequest_API,
    CancelRequest_API,
    Follow_API,
    Unfollow_API,

    PostList_API,
    PostDetail_API,
    PostLikes_API,

    CommentList_API,
    CommentDetail_API,

    PhotoList_API,
    PhotoDetail_API,

    PhotoCommentList_API,
    PhotoCommentDetail_API,

    T_PostList_API,
    # T_CommentList_API,

)

from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView,
	)

urlpatterns = [
    path('register/', Register_API.as_view(), name='register'),
    path('login/', Login_API.as_view(), name='login'),
    path('token-refresh/', TokenRefreshView.as_view(), name='refresh-token'),




    path('main-user/', MainUser_API.as_view(), name='main-user'),
    path('main-user/changepassword', ChangePassword_API.as_view(), name='main-user-password'),
    path('main-account/', MainAccount_API.as_view(), name='main-account'),
    path('main-profile/', MainProfile_API.as_view(), name='main-profile'),


    path('main-request/', MainRequest_API.as_view(), name='main-request'),
    path('main-request/<int:request_id>/accept', MainRequest_Accept_API.as_view(), name='main-request-accept'),
    path('main-request/<int:request_id>/cancel', MainRequest_Cancel_API.as_view(), name='main-request-cancel'),

    path('main-relationship/', MainRelationship_API.as_view(), name='main-relationship'),
    path('main-follow/', MainFollow_API.as_view(), name='main-follow'),
    # path('main-follower/', MainFollower.as_view(), name='main-follower'),



#USER LIST
    path('userlist/', UserList_API.as_view(), name='user-list-global'),
    # path('userlist/?search=""', UserList_API.as_view(), name='user-list'),

#USER DETAIL
    path('userdetail/<int:user_id>', UserDetail_API.as_view(), name='user-detail-id'),
    path('userdetail/pu/<str:user_pu>', UserDetail_API.as_view(), name='user-detail-pu'),

    path('userdetail/<int:user_id>/sendrequest', SendRequest_API.as_view(), name='send-request'),
    path('userdetail/<int:user_id>/cancelrequest', CancelRequest_API.as_view(), name='cancel-request'),

    path('userdetail/<int:user_id>/follow', Follow_API.as_view(), name='follow'),
    path('userdetail/<int:user_id>/unfollow', Unfollow_API.as_view(), name='unfollow'),


    # path('userdetail/<int:user_id>/block', block_API.as_view(), name='block'),
    # path('userdetail/<int:user_id>/unblock', unblock_API.as_view(), name='unblock'),





#################################################

#POST LIST
    path('postlist/', PostList_API.as_view(), name='post-list-global'),
    #path('postlist/?search=""', PostList_API.as_view(), name='post-list-global'),
    #path('postlist/?following=true', PostList_API.as_view(), name='post-list-follow-only'),
    path('userdetail/<int:user_id>/postlist/', PostList_API.as_view(), name='post-list'),
    
#POST PostDetail_API
    path('postdetail/<int:pk>', PostDetail_API.as_view(), name='post-detail'),
    path('postdetail/<int:pk>/likelist', PostLikes_API.as_view(), name='post-likes'),

#POST's PHOTO HANDLER
    # path('postdetail/<int:post_id>/postphotolist')
    # path('postphotodetail/<int:postphoto_id>')
    


#COMMENT LIST
    path('postdetail/<int:post_id>/commentlist/', CommentList_API.as_view(), name='comment-list'),
#COMMENT DETAIL
    path('commentdetail/<int:comment_id>', CommentDetail_API.as_view(), name='comment-detail'),


#################################################

# #PHOTO LIST
#     path('photolist/', PhotoList_API.as_view(), name='photo-list-global'),
#     path('userdetail/<int:user_id>/photolist/', PhotoList_API.as_view(), name='photo-list'),

# #PHOTO DETAIL
#     path('photodetail/<int:photo_id>', PhotoDetail_API.as_view(), name='photo-detail'),

# #PHOTO COMMENT LIST
#     path('photodetail/<int:photo_id>/photocommentlist/', PhotoCommentList_API.as_view(), name='photo-comment-list'),

# #PHOTO COMMENT DETAIL
#     path('photocommentdetail/<int:photocomment_id>', PhotoCommentDetail_API.as_view(), name='photo-comment-detail'),

#################################################













    ###########TESTING

    path('t_postlist/', T_PostList_API.as_view(), name='post-list-t'),
    # path('t_postdetail/<int:post_id>/imagelist')
    # path('t_postdetail/<int:post_id>/imagedetail/<int:image_id>')
    
    # path('t_postdetail/<int:post_id>/commentlist/', T_CommentList_API.as_view(), name='comment-list-t'),
    # path('t_commentdetail/<int:comment_id>/imagelist/')
    # path('t_commentdetail/<int:comment_id>/imagedetail/<int:image_id>')

]

# queryparams = 
# search , filter , order by

# kwargs =
# specific_id