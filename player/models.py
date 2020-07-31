from django.db import models
from datetime import date

from django.contrib.auth.base_user import BaseUserManager,AbstractBaseUser
# Create your models here.

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username,phno , password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')
		if not phno:
			raise ValueError('Users must have a contact number')
		if not password:
			raise ValueError('Password cannot be Empty')
		user = self.model(
			email=self.normalize_email(email),
			username=username,
			phno = phno,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email,phno, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			username=username,
			password=password,
			phno = phno,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user
    

class Accounts(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email",max_length=100,unique=True,primary_key=True)
	username 				= models.CharField(max_length=70)
	phno                    = models.CharField(max_length=20)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username','phno']
	EMAIL_FIELD='email'

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

class Contact(models.Model):
    username=models.CharField(max_length=70)
    email=models.EmailField(max_length=100)
    subject=models.CharField(max_length=100)
    feedback=models.TextField()
    date = models.DateField(default=date.today)

def song_path(instance,filename):
	return('{0}/{1}'.format(instance.artist,filename))
class Songs(models.Model):
	song_title=models.CharField(max_length=70)
	artist=models.CharField(max_length=70)
	song_path=models.FileField(upload_to=song_path)
	date=models.DateField(default=date.today)


class Artist(models.Model):
	artist=models.CharField(primary_key=True,max_length=70)
	image=models.ImageField(upload_to=song_path,null=False)
	date=models.DateField(default=date.today)

