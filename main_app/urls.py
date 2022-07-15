from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'), # about route
    path('cats/', views.cats_index, name='index'), # index Route
    path('cats/<int:cat_id>/', views.cats_detail, name='detail'), # detail or show Route
    path('cats/create/', views.CatCreate.as_view(), name='cats_create'), # Create Route
    path('cats/<int:pk>/update/', views.CatUpdate.as_view(), name='cats_update'), # Update route
    path('cats/<int:pk>/delete/', views.CatDelete.as_view(), name='cats_delete'), # Delete route
    path('cats/<int:cat_id>/add_feeding/', views.add_feeding, name='add_feeding'), # create Feeding route
    path('toys/', views.ToyList.as_view(), name='toys_index'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
    # associate a toy with a cat (M:M)
    path('cats/<int:cat_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
]