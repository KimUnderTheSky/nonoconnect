from django.urls import path
from .views import *

app_name = "posting"

urlpatterns = [
    path('feed/', Feed_View_Set.as_view(), name='feed-view-set'),  
    path('feed/<int:feed_id>/', Feed_View_Set.as_view(), name='feed-view-set-update-delete'), 
    path('feed/<int:feed_id>/comment', Comment_View_Set.as_view(), name='comment-view-set'), 
    path('feed/<int:feed_id>/comment/<int:comment_id>/', Comment_View_Set.as_view(), name='comment-view-set-update-delete'),
    # 피드 이미지 리스트 생성
    path('feed/<int:feed_id>/images/', Feed_View_Set.as_view(), name='feed-view-set-update-delete'),     
]