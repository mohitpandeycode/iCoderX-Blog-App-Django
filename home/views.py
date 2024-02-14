from django.shortcuts import render, HttpResponse,redirect
from .models import Contact
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def home(request):
    top_posts = Post.objects.order_by('-views')[:3]
    return render(request,'home/index.html', {'toppost':top_posts})

def contact(request):
   
   if request.method == "POST":
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    content = request.POST['content']
    if len(content)<10:
       messages.error(request, "Please fill the information correct!")
    else:
        contact = Contact(name=name,email=email,phone=phone,content=content)
        contact.save()
        messages.success(request, "Thank you for contacting us. We will talk you via email soon...")
   return render(request,'home/contact.html')

def about(request): 
    return render(request,'home/about.html')

def search(request):
   query = request.GET["query"]
   if len(query)>30:
        allPost = Post.objects.none()
   else:
        allPosttitle = Post.objects.filter(title__icontains=query)
        allPostcontent = Post.objects.filter(content__icontains=query)
        allPost = allPosttitle.union(allPostcontent)
   if allPost.count() == 0:
        messages.warning(request, "No search results found....")
   params = {'allPost':allPost,'query':query}
   return render(request, 'home/search.html',params)


# create the signup functionality..
def handleSignUp(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
#check the error field signup
        if len(username)>10 :
            messages.error(request, "username must be under 10 charecters!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " username must be contain alphanumeric charecters (abc123)!")
            return redirect('home') 
        
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
        
# creating user after sign in

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your Account has been created successfully!")
        return redirect('home')
    else:
        return HttpResponse("error 404-not found")

# Create the log in functionality 
def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']   
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Login Succesfully!")
            return redirect('home')
        if len(loginusername)==0 and len(loginpassword)==0:
            messages.error(request,"error - Username or Password can not empty!")
            return redirect('home')
        else:
            messages.error(request,"Wrong Username or Password! Try again...")
            return redirect('home')

    return render(request,)

# Create the log out functionality 
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged out!")
    return redirect('home')
