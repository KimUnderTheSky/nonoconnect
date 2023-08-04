from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed, Comment, User
# Create your views here.
class Main(APIView):
    # 메인화면 피드 불러오기
    def get(self, request):
        try:
            # session에 user_id값이 없으면 에러
            user_id = request.session.get('user_id', None)
            if user_id is None:
                return JsonResponse ({'message':'NOSESSION_ERROR'}, status = 400)
            
            # 해당 사용자 유저 정보 불러오기
            user = User.objects.filter(user_id = user_id).first()

            #모든 피드 데이터 불러오기
            feed_object_list = Feed.objects.all().order_by("-feed_id")
            feed_list = []
            for feed in feed_object_list: 
                #피드를 쓴 user 객체 생성
                user = User.objects.filter(user_id= feed.user_id.user_id).first() 
                # 피드에 달린 댓글 전부가져오기
                comment_object_list = Comment.objects.filter(feed_id=feed.feed_id) 
                comment_list = []
                for comment in comment_object_list:
                    # 댓글을 쓴 유저 객체 가져오기
                    user = User.objects.filter(user_id=comment.user_id).first() 
                    comment_list.append(dict(feed_id = comment.feed_id,
                                        user_id=user.user_id,
                                        comment_id=comment.comment_id,
                                        user_nickname = user.nickname,
                                        context = comment.context,
                                        ))
                
                feed_list.append(dict(id=feed.feed_id,
                                    title = feed.title,
                                    context=feed.context,
                                    nickname=user.nickname,
                                    longitude=user.longitude,
                                    latitude=user.latitude,
                                    comment_list=comment_list,
                                    ))
            
            return JsonResponse({"feeds": feed_list, "user": user.user_id})
        except:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)

        

class Feed_View_Set(APIView):
    # 피드 생성
    def post(self, request):
        try: 
            user_id = request.data.get("user_id")
            title = request.data.get('title')
            context = request.data.get('context')
            longitude = request.data.get('longitude')
            latitude = request.data.get('latitude')

            Feed.objects.create(
                user_id = user_id,
                title = title,
                context = context,
                status = True,
                longitude = longitude,
                latitude = latitude )
            
            return JsonResponse({"message": "Feed created successfully."})
        except:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)            
    # 피드 업데이트
    def patch(self, request, feed_id):
        try:
            # 피드의 ID를 가져오기
            if feed_id is None:
                return JsonResponse({"message": "feed_id is required."}, status=400)

            # 피드의 ID를 기준으로 해당 피드를 가져오기.
            feed = Feed.objects.filter(feed_id=feed_id).first()
            if feed is None:
                return JsonResponse({"message": "Feed not found."}, status=404)

            # 수정할 필드를 가져오기
            title = request.data.get("title")
            context = request.data.get("context")
            longitude = request.data.get("longitude")
            latitude = request.data.get("latitude")

            # 수정할 필드를 업데이트
            if title is not None:
                feed.title = title
            if context is not None:
                feed.context = context
            if longitude is not None:
                feed.longitude = longitude
            if latitude is not None:
                feed.latitude = latitude

            # 변경사항 저장
            feed.save()

            return JsonResponse({"message": "Feed updated successfully."})
        except:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)                
    #피드 삭제
    def delete(self, request, feed_id):
        try:
            # 피드의 ID를 가져오기
            if feed_id is None:
                return JsonResponse({"message": "feed_id is required."}, status=400)

            # 피드의 ID를 기준으로 해당 피드를 가져오기.
            feed = Feed.objects.filter(feed_id=feed_id).first()
            if feed is None:
                return JsonResponse({"message": "Feed not found."}, status=404)

            feed.status = False  # status를 False로 저장

            # 변경사항을 저장
            feed.save()

            return JsonResponse({"message": "Feed deleted successfully."})
        except:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)                

class Comment_View_Set(APIView):
    # 댓글 생성
    def post(self, request, feed_id):
        try:
            user_id = request.data.get("user_id")
            feed_id = request.data.get('feed_id')
            context = request.data.get('context')

            Comment.objects.create(
                user_id = user_id,
                feed_id = feed_id,
                context = context,
                status = True )
            
            return JsonResponse({"message": "Comment created successfully."})
        except:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)                
    # 댓글 업데이트
    def patch(self, request, feed_id, comment_id):
        try:
            # 피드의 ID를 가져오기
            if comment_id is None:
                return JsonResponse({"message": "comment_id is required."}, status=400)

            # 댓글의 ID를 기준으로 해당 댓글을 가져오기.
            comment = Comment.objects.filter(comment_id=comment_id).first()
            if comment is None:
                return JsonResponse({"message": "Comment not found."}, status=404)

            # 수정할 필드를 가져오기
            context = request.data.get("context")

            # 수정할 필드를 업데이트
            if context is not None:
                comment.context = context


            # 변경사항 저장
            comment.save()

            return JsonResponse({"message": "Comment updated successfully."})
        except:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)    
    #댓글 삭제
    def delete(self, request, feed_id, comment_id):
        try:            
            # 댓글의 ID를 가져오기
            if comment_id is None:
                return JsonResponse({"message": "comment_id is required."}, status=400)

            # 댓글의 ID를 기준으로 해당 댓글을 가져오기.
            comment = Comment.objects.filter(comment_id=comment_id).first()
            if comment is None:
                return JsonResponse({"message": "Comment not found."}, status=404)

            comment.status = False  # status를 False로 저장

            # 변경사항을 저장
            comment.save()

            return JsonResponse({"message": "Comment deleted successfully."})    
        except:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)            