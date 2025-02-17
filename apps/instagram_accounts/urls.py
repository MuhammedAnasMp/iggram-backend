from django.urls import path
from .views import IgLoginClassView ,UserInstagramAccountsView
from .utils import proxy_image
urlpatterns = [
    path('post_ig_data', IgLoginClassView.as_view() ),
    path("accounts", UserInstagramAccountsView.as_view()),
    path("proxy-image",proxy_image ),
]