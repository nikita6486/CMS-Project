from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# class User(AbstractUser):

#     GENDER_CHOICES = [
#         ('male', 'male'),
#         ('female', 'female'),
#         ('nonbinary', 'nonbinary'),
#         ('prefer not to say', 'prefer not to say'),
#     ]

#     name = models.CharField(null=True, blank=True, max_length=128)
#     email = models.EmailField(null=True, blank=True, max_length=128)
#     password = models.CharField(max_length=128)
#     gender = models.CharField(null=True, blank=True, max_length=128, choices=GENDER_CHOICES)
#     bio = models.TextField(null=True,blank=True)
#     profile_picture = models.ImageField(upload_to='user_profiles/', null=True, blank=True)
#     created_at = models.DateTimeField(null=True, auto_now_add=True)
#     updated_at = models.DateTimeField(null=True, auto_now=True)
#     deleted_at = models.DateTimeField(null=True)

#     def __str__(self):
#         return str(self.email) + ' - id - ' + str(self.id)
    
class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('nonbinary', 'Non-Binary'),
        ('prefer_not_to_say', 'Prefer Not to Say'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    gender = models.CharField(null=True, blank=True, max_length=128, choices=GENDER_CHOICES)
    bio = models.TextField(null=True, blank=True)
    username = models.CharField(null=True, blank=True, max_length=128, unique=True)
    profile_picture = models.ImageField(upload_to='user_profiles/', null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.email) + ' - id - ' + str(self.id)
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    is_public = models.BooleanField(default=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
    
class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    comment = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True)