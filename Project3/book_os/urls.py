from django.urls import path, re_path
from .views import Login, Index, Book, Press


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('index/', Index.as_view(), name='index'),
    path('book/<str:operation>/', Book.as_view(), name='book'),
    path('author/<str:operation>/', Book.as_view(), name='author'),
    path('press/<str:operation>/', Press.as_view(), name='press'),

]
