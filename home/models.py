from distutils.command.upload import upload
from operator import mod, truediv
from pyexpat import model
from sre_constants import CATEGORY
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import * 


11
# Create your models here.
GENDER =(
    ('male','male'),
    ('female','female'),
)

class Reader(models.Model):
    user = models.OneToOneField( User, on_delete=models.CASCADE)
    name = models.CharField(max_length=122)
    gender = models.CharField(max_length=7, choices= GENDER, null=True,blank=True)
    phone = models.CharField(max_length=122 ,null=True,blank=True)
    city = models.CharField(max_length=122,null = True, blank=True)
    age = models.CharField(max_length=3,null = True, blank=True)
    user_img = models.ImageField( upload_to ="userImg",default='userImg/default.png', null = True,blank=True)

    def __str__(self) :
        return str(self.id)


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    category_img = models.ImageField(upload_to='categoryimg')

    def __str__(self):
        return str(self.category_name)

class Book_details(models.Model):
    book_title = models.CharField(max_length=300)
    book_author = models.CharField(max_length=300)
    book_desc = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    book_page = models.IntegerField()
    book_lng = models.CharField(max_length=60)
    book_file = models.FileField(upload_to='documents/')
    book_img = models.ImageField(upload_to='bookimg/')
    book_upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Saved_book(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    books = models.ForeignKey(Book_details, on_delete=models.CASCADE)



REQ_STATUS =(
    ('pending','pending'),
    ('accepted','accepted'),
    ('rejected','rejected'),
    ('success','success'),
)
class Book_request(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=2)
    book_name = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    req_date = models.DateTimeField(auto_now_add=True)
    req_status = models.CharField(max_length=200,default='pending' ,choices = REQ_STATUS)