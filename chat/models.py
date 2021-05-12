from django.db import models

class UserAccount(models.Model):
    Email=models.EmailField(max_length = 254)
    UserID=models.TextField(max_length=30)
    Password=models.TextField(max_length=30)
    FriendList=models.TextField()
    ProfilePicture=models.ImageField()
    objects = models.Manager() 
