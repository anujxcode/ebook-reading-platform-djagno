from django.contrib import admin
from home.models import *

# Register your models here.
class AdminCategory(admin.ModelAdmin):
    list_display =('id','category_name','category_img')

admin.site.register(Category,AdminCategory)

class AdminReader(admin.ModelAdmin):
    list_display =('user','name','phone','city','age')

admin.site.register(Reader,AdminReader)

class AdminBook(admin.ModelAdmin):
    list_display =('id','book_title','book_author','category','book_upload_date')

admin.site.register(Book_details,AdminBook)


class AdminSavedbook(admin.ModelAdmin):
    list_display =('id','user','books')
admin.site.register(Saved_book,AdminSavedbook)

class AdminRequest(admin.ModelAdmin):
    list_display =('id','book_name','author_name','req_date')
    
admin.site.register(Book_request,AdminRequest)
