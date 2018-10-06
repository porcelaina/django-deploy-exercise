from django.db import models
#from django.contrib.auth import User -> 이렇게 하니 에러남. cannot import name 'User'. 아래처럼 .models를 추가해줘야..Django 2로 버전업되면서 바뀐건지? 20181005
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):

    # user = models.OneToOneField(User) -> 이렇게 하니 에러남. Django 2 부터는 on_delete 속성을 필수로 지정해줘야. 보통은 models.CASCADE로 한다는듯..20181005
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional classes
    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pic', blank=True)

    def __str__(self):
        return self.user.username # 여기서의 username은 User class의 내장 속성임

