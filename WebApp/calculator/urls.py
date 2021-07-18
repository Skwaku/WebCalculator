from django.urls import path



from . import views

"""create url(s) of the views function(s)"""
urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('calculator/', views.user_calculator, name='calculator'),
    path('history/', views.user_history, name='history'),
]
