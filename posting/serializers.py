from rest_framework import serializers
from posting.models import Feed, Feed_image, Comment, Comment_image


class FeedImageSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Feed_image
        fields = ['image']


class FeedSerializer(serializers.ModelSerializer):

    images = FeedImageSerializer(many=True, read_only=True)
    print(images)

    class Meta:
        model = Feed
        fields = ['feed_id', 'title', 'context', 'created_date', 'updated_date', 'status', 'longitude', 'latitude', 'user_id','images']
        
        
    def create(self, validated_data):
        print(self)
        print(validated_data)
        # 이미지들을 context의 request.FILES에서 가져옵니다.
        image_set = self.data.getlist('FILES')

        # Feed 객체를 생성하고 저장합니다.
        feed = Feed.objects.create(
            title=self.data.get('title'),
            context=self.data.get('context'),
            status=True,
            longitude=self.data.get('longitude'),
            latitude=self.data.get('latitude'),
            user=self.data.get('user_id'),
        )

        # 이미지들을 Feed_image 모델에 저장합니다.
        for image_data in image_set:
            Feed_image.objects.create(feed=feed, image=image_data)

        return feed