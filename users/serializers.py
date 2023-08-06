from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer) :
    #password = serializers.CharField(max_length=300, verbose_name="비밀번호")
    # name = serializers.CharField(max_length=64, verbose_name="이름")
    # email = serializers.EmailField(max_length=128, unique=True, verbose_name="사용자 이메일")
    # createdDate = serializers.DateTimeField(auto_now_add=True, verbose_name="생성일자")
    # modifiedDate = serializers.DateTimeField(auto_now=True, verbose_name="수정일자")
    # birthdate = serializers.DateTimeField()
    # nickname = serializers.CharField(max_length=64, unique=True, verbose_name="이름")
    # profileImage = serializers.ImageField()
    # phone = serializers.CharField(max_length=15, unique=True, verbose_name= "전화번호")

    
    class meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user

    