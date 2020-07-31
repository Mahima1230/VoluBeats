from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [
   path('', views.index , name ='index'),
   path('index.html', views.index , name ='index'),
   path('register.html', views.register , name ='register'),
   path('login.html', views.login , name ='login'),
   path('contact.html', views.contact , name ='contact'),
   path('logout.html', views.logout , name ='logout'),
   path('albums-store.html', views.albums , name ='albums'),
   path('albums-store/<artist_name>', views.albums , name ='album'),
   path('albums-store', views.load_artist , name ='loadalbums'),
   path('puttingsongs.html',views.puttingsongs,name='puttingsongs'),
   path('Add_artist.html',views.add_artist,name='add_artist'),
   path('Add_artist.html',views.add_artist,name='add_artist'),
  #  path('artist/<artist_name>',views.song,name='song'),
   path('forgot_password.html', views.forgotpass , name ='forgotpass'),
   path('Change_Password.html', views.changepassword , name ='changepassword'),

   

 ]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)