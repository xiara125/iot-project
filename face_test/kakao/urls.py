from django.contrib import admin
from django.urls import path
from django.urls.resolvers import URLPattern
from kakao.views import *

urlpatterns = [
    path('login/',KaKaoLoginView.as_view(), name="login"),
    path('oauth/',KakaoAuthView.as_view(), name="oauth"),
    path('talk/',KakaoTalkView.as_view(),name="talk")
]

