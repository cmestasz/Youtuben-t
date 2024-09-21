from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.Search.as_view(), name='search'),
    path('play/', views.Play.as_view(), name='play'),
    path('cached-list/', views.CachedAudioViewSet.as_view(), name='cached-list'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('save/', views.Save.as_view(), name='save'),
    path('forget/', views.Forget.as_view(), name='forget'),
    path('saved-list/', views.SavedList.as_view(), name='saved-list'),
]