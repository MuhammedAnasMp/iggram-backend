from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('session_check_view', views.session_check_view, name='session_check'),
    path('csrf-token/', views.csrf_token_view, name='csrf_token'),
        
    path('verify-token', views.verifytoken, name='verify-token'),
    
    path('publicview', views.PublicView.as_view(), name='public view'),
    
    path('logout', views.logout_view, name='logout_view'),
    
    
    
]
