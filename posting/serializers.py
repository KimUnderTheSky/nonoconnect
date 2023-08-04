from rest_framework import serializers
from posting.models import Feed, Feed_image, Comment, Comment_image


class FeedImageSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Feed_image
        fields = ['image']


class FeedSerializer(serializers.ModelSerializer):

    images = FeedImageSerializer(many=True, read_only=True)


    class Meta:
        model = Feed
        fields = ['feed_id', 'title', 'context', 'created_date', 'updated_date', 'status', 'longitude', 'latitude']
        
        
    def create(self, validated_data):
        instance = Feed.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            Feed_image.objects.create(Feed=instance, image=image_data)
        return instance