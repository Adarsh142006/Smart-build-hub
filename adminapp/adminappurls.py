from django.urls import path
from.import views
urlpatterns =[
    path('admindash/',views.admindash,name='admindash'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('viewenq/',views.viewenq,name='viewenq'),
    path('viewenq/<id>',views.delenq,name='delenq'),
    path('changepass/',views.changepass,name='changepass'),
    path('managecontractors/',views.managecontractors,name='managecontractors'),
    path('managehomeowners/',views.managehomeowners,name='managehomeowners'),

    

]