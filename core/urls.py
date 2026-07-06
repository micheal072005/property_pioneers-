from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),


     # Admin Authentication
    path('only_admin_login/', views.admin_login, name='admin_login'),
    path('only_admin_logout/', views.admin_logout, name='admin_logout'),



    path('dashboard/messages/', views.messages_dashboard, name='messages_dashboard'),
    path('dashboard/reply/<slug:slug>/', views.reply_message, name='reply_message'),

    path('properties/', views.property_list, name='property_list'),
    path('property/<slug:slug>/', views.property_detail, name='property_detail'),
    path('add-property/', views.add_property, name='add_property'),
    path('edit-property/<slug:slug>/', views.add_property, name='edit_property'),  # Same view!
    path('delete-property/<slug:slug>/', views.delete_property, name='delete_property'),
]
