from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [

    path('',views.index, name="home"),
    path('index/',views.index, name="home"),
    path('books/',views.books, name="books"),
    path('rating/',views.rating, name="rating"),
    path('about/',views.about, name="about"),
    path('contact/',views.contact, name="contact"),
    path('savedbook/',views.savedbook, name="savedbook"),
    path('profile/',views.profile, name="profile"),
    path('request/',views.request, name="request"),
    path('bookdetails/<str:pk_test>/', views.bookdetails, name="bookdetails"),
    path('books/bookdetails/<str:pk_test>/', views.bookdetails, name="bookdetails"),
    path('remove_saved_book/<str:sbid>/', views.remove_saved_book, name="remove_saved_book"),
    path('profile_edit/<str:uid>/', views.profile_edit, name="profile_edit"),
    path('pdfviewer/', views.pdfviewer, name="pdfviewer"),
]
