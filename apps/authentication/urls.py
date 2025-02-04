from django.urls import path
from . import views
from .views import ProtectedView
urlpatterns = [
    path('', views.index, name='index'),



    path('api/verify-firebase-token/', views.verify_firebase_token, name='verify_firebase_token'),

    path('api/protected/', ProtectedView.as_view(), name='protected'),  
    
    path('git-pull', views.git_pull, name='git_pull')
    
]
