from django.urls import path 
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name='index'),
    path("sign_in/", views.sign_in, name="sign_in"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post_image/', views.post_image, name='post_image'),
    path('update_image/<int:image_id>/', views.update_image, name='update_image'),
    path('delete_image/<int:image_id>/', views.delete_image, name="delete_image"),
    path('rate_art_entry/<int:art_entry_id>/', views.rate_art_entry, name='rate_art_entry'),
    path('get_user_rating/<int:art_entry_id>/', views.get_user_rating, name='get_user_rating'),
    path('signout/', auth_views.LogoutView.as_view(next_page='index'), name='signout'),
]