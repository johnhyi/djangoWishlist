from django.urls import path
from wishlist_app import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wishlist', views.wishlist),
    path('logout', views.logout),
    path('additem', views.additem),
    path('items', views.items),
    path('createitem', views.createitem),
    path('produceitem', views.produceitem),
    path('home', views.home),
    path('wishitem/<int:item_id>', views.wishitem),
    path('removeitem/<int:item_id>', views.removeitem),
    path('item/<int:item_id>', views.wish)
]
