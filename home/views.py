from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
	return render(request,'home/home.html')

def contact(request):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		phone = request.POST['phone']
		content = request.POST['content']

		if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
			messages.error(request,"Please fill the form correctly.")
		contact = Contact(name=name,email=email,phone=phone,content=content)
		contact.save()
	return render(request,'home/contact.html')

def about(request):
	return render(request,'home/about.html')

def search(request):
	query = request.GET['query']
	if len(query) > 100 or len(query) == 0:
		queryPosts = Post.objects.none()
	
	else:
		queryPostsTitle = Post.objects.filter(title__icontains = query)
		queryPostsContent = Post.objects.filter(content__icontains=query)
		queryPosts = queryPostsTitle.union(queryPostsContent)

	if queryPosts.count() == 0:
		messages.warning(request,"No Search Results. Enter Query Again.")
	
	params = {'queryPosts' : queryPosts} 
	return render(request,'home/search.html',params)


def handleSignUp(request):
	if request.method == 'POST':
		username = request.POST['username']
		fname = request.POST['fname'] 
		lname = request.POST['lname']
		email = request.POST['email']
		pass1 = request.POST['pass1']
		pass2 = request.POST['pass2']

		if len(username) > 10:
			messages.error(request,"username must be less than 10 characters.")
			return redirect('home')

		if  not username.isalnum():
			messages.error(request,"username should only contain letters and numbers characters.")
			return redirect('home') 

		if pass1 != pass2:
			messages.error(request,"Please Enter same password")
			return redirect('home')


		myuser = User.objects.create_user(username,email,pass1)
		myuser.first_name = fname
		myuser.last_name = lname
		myuser.save()
		messages.success(request,"Your Icoder Account has been created successfully.")
		return redirect('home')
	else:
		return HttpResponse('404- Not Found')


def handleLogin(request):
	if request.method == 'POST':
		loginusername = request.POST['loginusername']
		loginpass = request.POST['loginpass'] 

		user = authenticate(username=loginusername, password=loginpass)

		if user is not None:
			login(request,user)
			messages.success(request,"Logged in successfully")
			return redirect('home')
		else:
			messages.error(request,"Invalid Credentials.")
			return redirect('home')

	else:
		return HttpResponse('404- Not Found')


def handleLogout(request):
	logout(request)
	messages.success(request, "Logged out successfully.")
	return redirect('home')	