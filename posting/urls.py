from django.urls import path
from .views import *

app_name = "posting"

urlpatterns = [
    # Feed
    path('feed', Feed_View_Set.as_view(), name='feed-view-set'),  
    path('feed/<int:feed_id>', Feed_View_Set.as_view(), name='feed-view-set-update-delete'), 
    # Comment
    path('feed/<int:feed_id>/comment', Comment_View_Set.as_view(), name='comment-view-set'), 
    path('feed/<int:feed_id>/comment/<int:comment_id>', Comment_View_Set.as_view(), name='comment-view-set-update-delete'),
    # Call
    path('feed/<int:feed_id>/call', Call_View_Set.as_view(), name='call-view-set')
]