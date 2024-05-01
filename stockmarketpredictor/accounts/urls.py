from django.urls import path
from . import views

urlpatterns = [    
    path('', views.register, name = 'register'),
    path('signin', views.signin, name = 'signin'),
    path('signout', views.signout, name = 'signout'),
    path('check_login_status/', views.check_login_status, name='check_login_status'),
    path('get_user_data/', views.get_user_data, name='get_user_data'),

]