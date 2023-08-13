from rest_framework import serializers
from posting.models import Feed, Feed_image, Comment, Comment_image 
from account.models import account
import os, uuid
from django.conf import settings
class FeedImageSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=False)

    class Meta:
        model = Feed_image
        fields = ['image']


class FeedSerializer(serializers.ModelSerializer):

    images = FeedImageSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Feed
        fields = ['feed_id', 'title', 'context', 'created_date', 'updated_date', 'status', 'longitude', 'latitude','images','user_id']


    def create(self, validated_data):
        # 이미지들을 context의 request.FILES에서 가져옵니다.
        image_set = self.context['request'].FILES.getlist("FILES")
        image_data = []
        user_id = self.context['request'].data['user_id']

        for image in image_set:
            # 이미지 파일 이름을 고유하게 만듦
            unique_filename = f"{uuid.uuid4().hex}{os.path.splitext(image.name)[1]}"

            # 이미지 파일을 MEDIA_ROOT에 저장
            file_path = os.path.join(settings.MEDIA_ROOT, "posting",unique_filename)
            with open(file_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # 이미지 파일의 URL을 image_data에 추가
            image_data.append({'image': os.path.join(settings.MEDIA_URL,"posting", unique_filename)})
        
        # User 인스턴스 가져오기
        user = account.objects.get(pk=user_id)  # user_id를 이용하여 User 인스턴스 가져오기

        # Feed 객체를 생성하고 저장합니다.
        feed = Feed.objects.create(
            title=self.data.get('title'),
            context=self.data.get('context'),
            status=True,
            longitude=self.data.get('longitude'),
            latitude=self.data.get('latitude'),
            user=user,
        )

        # 이미지들을 Feed_image 모델에 저장합니다.
        for image in image_data:
            Feed_image.objects.create(feed=feed, image=image["image"])

        return feed
    
    def update(self, instance, validated_data):
        # User 인스턴스 가져오기
        user_id = self.context['request'].data['user_id']  # 'user_id' 키의 값을 빼고 따로 저장
        user = account.objects.get(pk=user_id)  # user_id를 이용하여 User 인스턴스 가져오기

        # Feed 객체를 업데이트합니다.
        instance.title = self.data.get('title')
        instance.context = self.data.get('context')
        instance.status=True
        instance.longitude = self.data.get('longitude')
        instance.latitude = self.data.get('latitude')
        instance.user = user
        instance.save()

        # 기존 이미지 url 삭제 후, 업데이트(재생성)
        Feed_image.objects.filter(feed_id=instance.feed_id).delete()
        image_set = self.context['request'].FILES.getlist("FILES")
        image_data = []

        for image in image_set:
            # 이미지 파일 이름을 고유하게 만듦
            unique_filename = f"{uuid.uuid4().hex}{os.path.splitext(image.name)[1]}"

            # 이미지 파일을 MEDIA_ROOT에 저장
            file_path = os.path.join(settings.MEDIA_ROOT, "posting",unique_filename)
            with open(file_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # 이미지 파일의 URL을 image_data에 추가
            image_data.append({'image': os.path.join(settings.MEDIA_URL,"posting", unique_filename)})

        for image in image_data:
            Feed_image.objects.create(feed=instance, image=image["image"]) 

            updated_feed = Feed.objects.get(pk=instance.feed_id)

        return updated_feed
