from asyncio.windows_events import NULL
from asyncore import read
from email import message
import imp
from multiprocessing import context
from tkinter.messagebox import RETRY
from django.contrib import messages
from django.shortcuts import redirect, render
from home.models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.

# index page functions
def index(request):
    if request.method =='POST':
        if request.user.is_authenticated:
            user = request.user
            book = request.POST.get('reqbook')
            author = request.POST.get('reqauthor')
            bookreq = Book_request.objects.create(user = user,book_name = book ,author_name = author)
            bookreq.save()
            messages.success(request,"Request sent successfully, Go to Saved Book to see your request Status")
        else:
            messages.error(request,"To make a Book request login first ")
   
    cat = Category.objects.all()
    bookslist = Book_details.objects.all()
    return render(request,'index.html',{'category':cat,'bookslist':bookslist})


# fetching  book from Book_details table and Category from Category table
def books(request):
    books = Book_details.objects.all()

    if 'q' in request.GET:
        q = request.GET['q']
        squery = Q(Q(book_title__icontains = q) | Q(book_author__icontains = q))
        books = Book_details.objects.filter(squery)


    cat = Category.objects.all()
    CATID = request.GET.get('categories')
    if CATID:
        catName = Category.objects.get(id = CATID).category_name
        books = Book_details.objects.filter(category = CATID)
        return render(request,'books.html',{'books':books,'Category':cat,'catName':catName})
    
    
    return render(request,'books.html',{'books':books,'Category':cat})

# simple render about.html
def about(request):
    return render(request,'about.html')

# simple render contact.html
def contact(request):
    return render(request,'contact.html')

# show data of saved books 
def savedbook(request):
    if request.user.is_authenticated:
       
        if request.method =='POST':
            user = request.user
            book_id = request.POST.get('book_id')
            book = Book_details.objects.get(id = book_id)
            Saved_book(user = user,books = book).save()
            messages.success(request,'Book Saved Successfully !!!!')
            return redirect('/savedbook/')


        user = request.user
        savedbook = Saved_book.objects.filter(user = user)
        reqbook = Book_request.objects.filter(user = user)
        context ={
            'SB':savedbook,
            'reqbook':reqbook,
        }

        # if savedbook.count() == 0 :
        #     return render(request,'emptysaved.html')
        # else:
        return render(request,'savedbook.html', context)

    else :
        return redirect('/account/signin')

# @login_required
# remove form saved books
def remove_saved_book(request,sbid): 
    DELID = sbid
    delBook = Saved_book.objects.filter(id = DELID)
    delBook.delete() 
    return redirect('/savedbook/')


# fetching data user profile
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        reader = Reader.objects.filter(user = user)
        return render(request,'profile.html',{ 'rd':reader })
    else:
        return redirect('/account/signin')

# @login_required
is_book_saved = False
# show Book details 
def bookdetails(request, pk_test):
    book = Book_details.objects.get(id = pk_test)
    global is_book_saved
    if request.user.is_authenticated:
        is_book_saved = False
        is_book_saved = Saved_book.objects.filter(Q(user = request.user) & Q(books = book.id))
    
    context = { 'book':book,'is_book_saved':is_book_saved}
    return render(request,'bookdetails.html', context)

# @login_required
# render request.html wich contains a form to make a request
def request(request):
    return render(request,'request.html')

# @login_required
# edit profile or uplaod profile pic
def profile_edit(request,uid):
    
    if request.method =='POST': 
        if request.FILES.get('pro_pic'):
            pro_pic = request.FILES.get('pro_pic')
            fs = FileSystemStorage()
            imgUrl = fs.save( 'userImg/'+pro_pic.name,pro_pic)
        
            user = request.user
            userid = User.objects.get(username = user).id
            print(userid)
            reader = Reader(
                id = uid,
                user_id = userid,
                gender = request.POST.get('gender'),
                name = request.POST.get('name'),
                city = request.POST.get('city'),
                age = request.POST.get('age'),
                phone = request.POST.get('phone'),
                user_img = imgUrl
            )

            if request.user.is_superuser:
                updateuser = User(
                    id = userid,
                    username = user.username,
                    email = request.POST.get('email'),
                    password = user.password,
                    is_superuser = True,
                    is_staff = True
                )
            else:
                updateuser = User(
                    id = userid,
                    username = user.username,
                    email = request.POST.get('email'),
                    password = user.password,
                    is_superuser = False,
                    is_staff = False,
                )

            reader.save()
            updateuser.save()
        
            messages.success(request,'update sucessfully')
            return redirect('/profile/')

        else:
            imgUrl = request.POST.get('imgurl')
            url = imgUrl[7:]
            user = request.user
            userid = User.objects.get(username = user).id
            print(userid)
            reader = Reader(
                id = uid,
                user_id = userid,
                gender = request.POST.get('gender'),
                name = request.POST.get('name'),
                city = request.POST.get('city'),
                age = request.POST.get('age'),
                phone = request.POST.get('phone'),
                user_img = url
            )

            if request.user.is_superuser:
                updateuser = User(
                    id = userid,
                    username = user.username,
                    email = request.POST.get('email'),
                    password = user.password,
                    is_superuser = True,
                    is_staff = True
                )
            else:
                updateuser = User(
                    id = userid,
                    username = user.username,
                    email = request.POST.get('email'),
                    password = user.password,
                    is_superuser = False,
                    is_staff = False,
                )
                
            reader.save()
            updateuser.save()
        
            messages.success(request,'update sucessfully')
            return redirect('/profile/')

    updateID = Reader.objects.get(id = uid)
    return render(request,'profile_edit.html',{'uid':updateID})
