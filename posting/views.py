import uuid
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed, Comment, User, Feed_image, Call
from .serializers import FeedSerializer, FeedImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings


# Create your views here.
class Main(APIView):
    # 메인화면 피드 불러오기
    def get(self, request):
        # session에 user_id값이 없으면 에러 / 현재는 session대신 request에 user_id 값 사용
        user_id = request.data.get('user_id', None)
        if user_id is None:
            return JsonResponse ({'message':'NOSESSION_ERROR'}, status = 400)
        
        # 해당 사용자 유저 정보 불러오기
        user_info = User.objects.filter(id = user_id).first()
        if user_info:
            user_data = {
                "id": user_info.id,
                "nickname": user_info.nickname,
                "longitude": user_info.longitude,
                "latitude": user_info.latitude,
                "birthdate": user_info.birthdate,
                "profile_image": user_info.profileImage.url if user_info.profileImage else None,


                # 필요한 다른 사용자 정보도 추가
            }
        else:
            return JsonResponse({'message': 'User not found'}, status=404)
        

        #모든 피드 데이터 불러오기
        feed_object_list = Feed.objects.all().order_by("-feed_id")
        feed_list = []
        for feed in feed_object_list: 
            #피드를 쓴 user 객체 생성
            user = User.objects.filter(id= feed.user.id).first()
            # 피드에 달린 댓글 전부가져오기
            comment_object_list = Comment.objects.filter(feed_id=feed.feed_id) 
            comment_list = []
            for comment in comment_object_list:
                # 댓글을 쓴 유저 객체 가져오기
                user = User.objects.filter(id=comment.user.id).first() 
                comment_list.append(dict(feed_id = comment.feed.feed_id,
                                    user_id=user.id,
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
        
        return JsonResponse({"feeds": feed_list, "user": user_data})

class Feed_View_Set(APIView):
    def post(self, request):
        # request 내 데이터를 통해 FeedSerailizer 객체 생성
        serializer = FeedSerializer(data=request.data,  context={'request': request}) 
        print("serializer", serializer)
        # 유효성검사
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Feed is created."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    def get(self, request, feed_id):
            # 피드의 ID를 가져오기
            if feed_id is None:
                return Response({"message": "feed_id is required."}, status=status.HTTP_400_BAD_REQUEST)

            # 피드의 ID를 기준으로 해당 피드를 가져오기.
            feed = Feed.objects.filter(feed_id=feed_id).first()
            if feed is None:
                return Response({"message": "Feed not found."}, status=status.HTTP_404_NOT_FOUND)

            # Serializer를 사용하여 피드 정보를 JSON으로 변환(파이썬 객체 to Json)
            serializer = FeedSerializer(feed)

            # 피드 이미지 URL 정보 가져오기
            feed_images = Feed_image.objects.filter(feed_id=feed_id)
            image_urls = [img.image.url for img in feed_images]

            # JSON 응답에 이미지 URL 정보 추가하여 보내기
            response_data = serializer.data
            response_data['image_urls'] = image_urls

            comment_object_list = Comment.objects.filter(feed_id=feed.feed_id) 
            comment_list = []
            for comment in comment_object_list:
                # 댓글을 쓴 유저 객체 가져오기
                user = User.objects.filter(id=comment.user.id).first() 
                comment_list.append(dict(feed_id = comment.feed.feed_id,
                                    user_id=user.id,
                                    comment_id=comment.comment_id,
                                    user_nickname = user.nickname,
                                    context = comment.context,
                                    ))

            response_data['comments'] = comment_list    
            return Response(response_data, status=status.HTTP_200_OK)
    
    # 피드 업데이트
    def put(self, request, feed_id):

        # 피드의 ID를 가져오기
        if feed_id is None:
            return Response({"message": "feed_id is required."}, status=400)

        # 피드의 ID를 기준으로 해당 피드를 가져오기.
        feed = Feed.objects.filter(feed_id=feed_id).first()
        if feed is None:
            return Response({"message": "Feed not found."}, status=404)

        # Serializer를 생성할 때 context에 요청(request) 객체를 전달합니다.
        serializer = FeedSerializer(feed, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Feed is updated."}, status=status.HTTP_200_OK)


        
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
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)                  

class Comment_View_Set(APIView):
    # 댓글 생성
    def post(self, request, feed_id):
        try:
            user_id = request.data.get("user_id")
            # feed_id = request.data.get('feed_id')
            context = request.data.get('context')

            Comment.objects.create(
                user_id = user_id,
                feed_id = feed_id,
                context = context,
                status = True )
            
            return JsonResponse({"message": "Comment created successfully."})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)                 
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
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)   
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
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)   


        
class Call_View_Set(APIView):
    # 요청 생성
    def post(self, request, feed_id):
        try:
            feed = Feed.objects.filter(pk = feed_id).first()
            if feed.status == 0:
                return JsonResponse({"message": "feed already accepted call"})

            # Call이 요청상태이면 불가, Feed가 없으면 불가


            call_user_id = request.data.get("user_id")
            call_user = User.objects.filter(id = call_user_id).first()

            # 요청 기록 생성
            Call.objects.create(
                call_user = call_user,
                feed_id = feed_id,
                call_status = True)
            
            # 피드 수락됨 상태
            feed = Feed.objects.filter(feed_id=feed_id).first()            
            feed.status = False
            feed.save()

            return JsonResponse({"message": "Call created successfully."})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)     
        
    # 요청 취소
    def delete(self, request, feed_id):
        try:
            feed = Feed.objects.filter(pk = feed_id).first()
            if feed.status == 1:
                return JsonResponse({"message": "feed is wating call"})
        
            call_user_id = request.data.get("user_id")
            call_user = User.objects.filter(id = call_user_id).first()

            # 요청 기록 생성
            Call.objects.create(
                call_user = call_user,
                feed_id = feed_id,
                call_status = False)
            
            # 피드 대기 중 상태
            feed = Feed.objects.filter(feed_id=feed_id).first()          
            feed.status = True
            feed.save()

            return JsonResponse({"message": "Call canceled successfully."})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)   