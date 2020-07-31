from django.shortcuts import render,redirect
from django.contrib import messages,auth
import re
from .models import Accounts,Contact,Songs,Artist
from django.http import HttpResponse,FileResponse,Http404,HttpResponseRedirect,JsonResponse
import random
from music_player.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
import string
# Create your views here.

def index(request):
	if(not request.user.is_authenticated):
		return redirect("login.html")
	try:
		song=Songs.objects.latest('date')
		artists=Artist.objects.all()
		latest=Songs.objects.all()[::-1][0:6]
		popular_artist=Artist.objects.all()
		popular_artist=random.sample(list(popular_artist),k=8)
		return render(request,'index.html',{'song':song,'artists':artists,'new_hits':latest,'popular_artist':popular_artist})
	except:
		return render(request,'index.html')
def register(request):
	if request.method=='POST':
		username=request.POST['username']
		email=request.POST['email']
		phno=request.POST['phno']
		passwd=request.POST['pass1']
		repass=request.POST['pass2']
		regex='^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
		phno_regex="^[6-9]\d{9}$"
		
		if passwd!=repass:
			messages.info(request,"Password do not match")
			return render(request,'register.html')
		elif not re.search(regex,email):
			messages.info(request,"Email not valid")
			return render(request,'register.html')
		elif not re.search(phno_regex,phno):
			messages.info(request,"Contact number not valid")
			return render(request,'register.html')
		user=Accounts.objects.create_user(email=email,username=username,phno=phno,password=passwd)
		user.save()
		messages.info(request,"Successfully Registered")  
		return render(request,'login.html')
	
	return render(request,'register.html')
def contact(request):
	
	if request.method=='POST':
		username=request.POST['username']
		email=request.POST['email']
		subject=request.POST['subject']
		msg=request.POST['message']
		data=Contact(username=username,email=email,subject=subject,feedback=msg)
		data.save()
		messages.info(request,"feedback submitted")  
		return render(request,"index.html")
	return render(request,"contact.html")    
def login(request):
	if request.method=='POST':
		email=request.POST['email']
		password=request.POST['pass']
		
		if email and password:
			user=auth.authenticate(email=email,password=password)
			if user is not None:
				auth.login(request,user)
				print("user authenticated")
				return redirect("index.html")
			else:
				messages.info(request,'Invalid Password')
				return render(request,'login.html')

	return render(request,'login.html')
def logout(request):
	auth.logout(request)
	return redirect("/")
def albums(request,artist_name=None):
	from django.db.models import Q
	if(artist_name):
		search_res=Songs.objects.filter(artist=artist_name)
		artists=Artist.objects.all()
		return render(request,"albums-store.html",{'search':search_res,'artists':artists})
	if request.method=='POST':
		search=request.POST.get("search")
		print("search=",search)
		if search:
			search_res=Songs.objects.filter(Q(artist__icontains=search) | Q(song_title__icontains=search))
			print("search results",search_res)
			return render(request,"albums-store.html",{'search':search_res})
		return render(request,"albums-store.html")
	else:
		artists=Artist.objects.all()
		latest=Songs.objects.all().order_by('-date')[0:5]
		print("latest : ",latest)
		return render(request,"albums-store.html",{'latest':latest,'artists':artists})
def puttingsongs(request):
	if(request.user.is_admin):
		if(request.method=='POST'):
			artist_name=request.POST.get('artist_name').upper()
			song_list=request.FILES.getlist('song')
			for song_file in song_list:
				new_song=Songs(song_path=song_file,song_title=song_file.name,artist=artist_name)
				print(song_file)
				new_song.save()
			messages.info(request,"Song submitted")
			return render(request,"puttingsongs.html")
		return render(request,"puttingsongs.html")
	messages.info(request,"The page you requested is not accessible")
	return redirect('/')

def add_artist(request):
	if(request.user.is_admin):
		if(request.method=='POST'):
			artist_name=request.POST.get("artist_name").upper()
			artist_image=request.FILES.get("artistimage")
			new_artist=Artist(artist=artist_name,image=artist_image)
			new_artist.save()
			messages.info(request,artist_name+" artist added")
			return render(request,"Add_artist.html")
		artists=Songs.objects.values('artist').distinct()
		print("artists:",artists)
		return render(request,"Add_artist.html",{'artists':artists})
	messages.info(request,"The page you requested is not accessible")
	return redirect('index.html')



def load_artist(request):
	data={}
	# artist_songs=Songs.objects.filter(artist=artist_name).values()
	artists=Artist.objects.all()
	for artist in artists:
		data[artist.artist]=artist.image.name
	# print("artist songs name: ",data)
	return JsonResponse(data)

def forgotpass(request):
	# Forgot Password
	if 'otp_verify_dict' not in globals():
		global otp_verify_dict
		otp_verify_dict={}
	if request.method=='POST':
		forgot_pass_email=request.POST.get('forgot_pass_email')
		if Accounts.objects.filter(email=forgot_pass_email).exists:
			user_otp=request.POST.get('verify_otp')
			pass1=request.POST.get('pass1')
			pass2=request.POST.get('pass2')
			if user_otp and pass1 and pass2:
				if pass1!=pass2:
					print("Passwords do not match")
					messages.info(request,"Passwords do not match")
					return redirect("forgot_password.html")
				elif int(user_otp)==otp_verify_dict[forgot_pass_email]:
					u=Accounts.objects.get(email=forgot_pass_email)
					u.set_password(pass1)
					u.save()
					subject="Music Player"
					msg="Hi "+forgot_pass_email+",\nYour password has been changed successfully.\nIn case you have not changed report it to our Team.\nThank You"
					recepient=forgot_pass_email
					try:
						send_mail(subject,msg,EMAIL_HOST_USER,[recepient],fail_silently=False)
						# otp_verify_dict[forgot_pass_email]=otp
						# messages.info(request,"Email has been sent")
						# return render(request,"forgot_password.html",{'recepient':recepient,'otp':otp})
					except:
						print("Error in sending Email")
					del otp_verify_dict[forgot_pass_email]
					print("Password changed successfully")
					messages.info(request,"Password changed successfully")
					return render(request,"login.html")
			else:
				otp=random.randint(1000,9999)
				print("otp : ",otp)
				subject="Trouble Signing In to your Music Account?"
				msg="Hi "+forgot_pass_email+",\nYou indicated that you are having a trouble signing in to your Music Account.\nYour OTP for Password Change is '"+str(otp)+"'.\nIn case you have not changed report it to our Team."
				recepient=forgot_pass_email
				try:
					send_mail(subject,msg,EMAIL_HOST_USER,[recepient],fail_silently=False)
					otp_verify_dict[forgot_pass_email]=otp
					messages.info(request,"Email has been sent")
					return render(request,"forgot_password.html",{'recepient':recepient,'otp':otp})
				except:
					messages.info(request,"Error in Sending Email.\nPlease try again Later.")
					return redirect('login.html')
	return render(request,"forgot_password.html")

def changepassword(request):
	if not request.user.is_authenticated:
		return render(request,"login.html")
	if request.method=='POST':
		old_pass=request.POST.get('old_pass')
		new_pass=request.POST.get('new_pass')
		confirm_new_pass=request.POST.get('confirm_new_pass')
		if(old_pass and new_pass and confirm_new_pass):
			if not check_password(old_pass,request.user.password):
				messages.info(request,"Incorrect Old Password")
				return redirect("Change_Password.html")
			elif new_pass==confirm_new_pass:
				u=request.user
				u.set_password(new_pass)
				u.save()
				messages.info(request,"Password changed successfully")
				return render(request,"index.html")
			else:
				messages.info(request,"Passwords do not match")
				return redirect("Change_Password.html")

	return render(request,"Change_Password.html")