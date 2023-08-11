from django.db import models
from users.models import User


class Feed(models.Model):
    feed_id = models.BigAutoField(help_text="Feed ID", primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_in_feed') # FK, related_name을 id값으로 식별
    title = models.CharField(max_length=100)
    context = models.TextField(max_length=2000, null=True)  
    created_date = models.DateTimeField(auto_now_add=True) # 레코드 추가 시 자동 추가
    updated_date = models.DateTimeField(auto_now=True) # 레코드 변경 시 자동추가
    status = models.BooleanField(default=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    
    class Meta:
        db_table = 'Feed'

class Feed_image(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE,related_name='feed') # 다대일 관계 지정
    image = models.ImageField(default='media/posting/default_image.jpeg', upload_to='feed_images/', blank=True, null=True)

    class Meta:
        db_table = 'Feed_image'

class Comment(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='feed_in_comment') # 다대일 관계 지정
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_in_comment') # FK, related_name을 id값으로 식별
    comment_id = models.BigAutoField(help_text="Comment ID", primary_key=True)
    context = models.TextField(max_length=2000)  
    created_date = models.DateTimeField(auto_now_add=True) # 레코드 추가 시 자동 추가
    updated_date = models.DateTimeField(auto_now=True) # 레코드 변경 시 자동추가
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'Comment'

class Comment_image(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='comment') # 다대일 관계 지정
    image = models.ImageField(default='media/posting/default_image.jpeg', upload_to='feed_images/', blank=True, null=True)

    class Meta:
        db_table = 'Comment_image'

class Call(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='feed_in_call') # 다대일 관계 지정
    call_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_in_call') # FK, related_name을 id값으로 식별
    call_id = models.BigAutoField(help_text="Call ID", primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True) # 레코드 추가 시 자동 추가
    updated_date = models.DateTimeField(auto_now=True) # 레코드 변경 시 자동추가
    call_status = models.BooleanField(default=True)
    class Meta:
        db_table = 'Call'