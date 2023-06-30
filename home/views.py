from asyncio.windows_events import NULL
from asyncore import read
from email import message
from http.client import HTTPResponse
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
is_rated = False
# show Book details 
def bookdetails(request, pk_test):
    book = Book_details.objects.get(id = pk_test)
    highlight = Book_highlight.objects.filter(book = book)
    global is_book_saved

    # Rating variables 
    global is_rated
    is_rated = False
    bkrating = Book_rating.objects
    ratingCount = bkrating.filter(book = book.id).count()
    nullreview = bkrating.filter(book = book.id, book_review = "").count()
    reviewCount = ratingCount - nullreview
    sumRating = 0
    for x in bkrating.filter(book = book.id):
        sumRating = sumRating + x.book_rating 


    if ratingCount != 0 :
        avgrcl = str((sumRating / ratingCount))
        avgRating = avgrcl[0:3]
    else:
        avgRating = "0.0"


    allreview = bkrating.filter(book = book.id).exclude(book_review = "")
    
    yourRating =  NULL
    if request.user.is_authenticated:
        is_book_saved = False
        is_rated = False
        is_book_saved = Saved_book.objects.filter(Q(user = request.user) & Q(books = book.id))
        is_rated = Book_rating.objects.filter(Q(user = request.user) & Q(book = book.id )).exists()
        yourRating = Book_rating.objects.filter(Q(user = request.user) & Q(book = book.id ))  

   
    context = { 
        'book':book,
        'is_book_saved':is_book_saved,
        'is_rated':is_rated,
        'yourRating':yourRating,
        'ratingCount':ratingCount,
        'reviewCount':reviewCount,
        'avgRating':avgRating,
        'allreview':allreview,
        'highlight':highlight
        }

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
            # print(userid)
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
            # print(userid)
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


def rating(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            ratedUser = request.user
            ratedBook = request.POST.get('rated_book')
            rating = request.POST.get('rating')
            review = request.POST.get('review')
            strid = str(ratedBook)


            bookObj = Book_details.objects.get(id = ratedBook)

            rate = Book_rating.objects.create(
                user = ratedUser,
                book = bookObj,
                book_rating =  rating,
                book_review = review
            ) 
            rate.save()
            messages.success(request,"Thank you for rate this book")
            return redirect(f'/bookdetails/{strid}/')
        else:
            return redirect('/books/')
    else:
        return redirect('/account/signin/')




def pdfviewer(request):
    if request.user.is_authenticated:
        
        if request.method =='GET':
            bookurl = request.GET.get("bookurl")
        
        bookName = bookurl[17:]
        context = {
            'bookurl':bookurl,
            'bookName':bookName,
        }
        
        return render(request,'pdfviewer.html',context)
    

    else:
        return redirect('/account/signin/')
