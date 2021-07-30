from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone


class History(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    expression = models.CharField("expression", max_length=500, blank=True)
    result = models.CharField("result", max_length=500, blank=True)


    def __str__(self):
        return self.expression



# class Profile(models.Model):
#     user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
#     first_name = models.CharField("first_name", max_length=100, blank=True)
#     last_name = models.CharField("last_name", max_length=100, blank=True)
#     password = models.CharField(max_length=100)
#     date_updated = models.DateTimeField('date_updated',default=timezone.now)
#
#
#     def __str__(self):
#         return f'{self.user.username} Profile'


