from django.contrib import messages
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from lbms.models import Book
from lbms.decorators import login_required
from lbms.models import Admin

def login(request):
    context = {}
    if request.method == "POST":
        admin = Admin.objects.filter(email=request.POST['username'].lower(), password = request.POST['password']).first()
        if admin:
            request.session['admin'] = admin.id
            return HttpResponseRedirect('/')
        messages.add_message(request, messages.ERROR, 'Invalid email/password. Please provide valid credentials')
        return render(request, 'login.html', context)
    return render(request, 'login.html', context)

def signup(request):
    context = {}
    if request.method == "POST":
        password = request.POST['password']
        cnf_password = request.POST['cnf_password']
        if password != cnf_password:
            messages.add_message(request, messages.ERROR, 'Password does not matched')
            return redirect('signup')
        old_admin = Admin.objects.filter(email=request.POST['username'].lower()).first()
        if old_admin:
            messages.add_message(request, messages.ERROR, 'Username already registered.')
            return redirect('signup')
        Admin.objects.create(email=request.POST['username'].lower(), password = request.POST['password'])
        messages.add_message(request, messages.SUCCESS, 'Admin created, please login.')
        return redirect('login')
    return render(request, 'signup.html', context)

def logout(request):
    request.session.flush()
    return redirect('home')

@login_required
def view(request, id):
    context = {}
    book = Book.objects.filter(id=id).first()
    context['book'] = book
    return render(request, 'view.html', context)

@login_required
def edit(request, id):
    context = {}
    book = Book.objects.filter(id=id).first()
    print(book.publish_date)
    context['book'] = book
    if request.method == "POST":
        book_name = request.POST['name']
        author = request.POST['author']
        publish_date = request.POST['publish_date']
        Book.objects.filter(id=id).update(name=book_name, author=author, publish_date=publish_date)
        messages.add_message(request, messages.SUCCESS, 'Book updated successfully.')
        return redirect('home')
    return render(request, 'edit.html', context)

@login_required
def delete(request):
    context = {}
    if request.method == "POST":
        book_id = request.POST['book_id']
        Book.objects.filter(id=book_id).delete()
        messages.add_message(request, messages.SUCCESS, 'Book deleted successfully.')
        return JsonResponse({'data':True})
    return render(request, 'home.html', context)

@login_required
def create(request):
    context = {}
    if request.method == "POST":
        book_name = request.POST['name']
        author = request.POST['author']
        publish_date = request.POST['publish_date']
        Book.objects.create(name=book_name, author=author, publish_date=publish_date)
        messages.add_message(request, messages.SUCCESS, 'Book added successfully.')
        return redirect('home')
    return render(request, 'create.html', context)

# @login_required
def home(request):
    context = {}
    books = Book.objects.order_by('-id').all()
    context['books'] = books
    print(context['books'])
    return render(request, 'home.html', context)
